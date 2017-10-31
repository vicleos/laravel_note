
### Laravel `ENV` 加载源码分析:
- `ENV` 的加载功能由类 `\Illuminate\Foundation\Bootstrap\LoadEnvironmentVariables::class` 完成，它的启动函数为：
```php
public function bootstrap(Application $app)
{
    if ($app->configurationIsCached()) {
        return;
    }

    $this->checkForSpecificEnvironmentFile($app);

    try {
        (new Dotenv($app->environmentPath(), $app->environmentFile()))->load();
    } catch (InvalidPathException $e) {
        //
    }
}
```
- 如果我们在环境变量中设置了 `APP_ENV` 变量，那么就会调用函数 `checkForSpecificEnvironmentFile` 来根据环境加载不同的 `env` 文件：
```php
protected function checkForSpecificEnvironmentFile($app)
{
    if (php_sapi_name() == 'cli' && with($input = new ArgvInput)->hasParameterOption('--env')) {
        $this->setEnvironmentFilePath(
            $app, $app->environmentFile().'.'.$input->getParameterOption('--env')
        );
    }

    if (! env('APP_ENV')) {
        return;
    }

    $this->setEnvironmentFilePath(
        $app, $app->environmentFile().'.'.env('APP_ENV')
    );
}

protected function setEnvironmentFilePath($app, $file)
{
    if (file_exists($app->environmentPath().'/'.$file)) {
        $app->loadEnvironmentFrom($file);
    }
}
```
- `vlucas/phpdotenv` 源码解读 :
- `laravel` 中对 `env` 文件的读取是采用 `vlucas/phpdotenv` 的开源项目：
```php
class Dotenv
{
    public function __construct($path, $file = '.env')
    {
        $this->filePath = $this->getFilePath($path, $file);
        $this->loader = new Loader($this->filePath, true);
    }

    public function load()
    {
        return $this->loadData();
    }

    protected function loadData($overload = false)
    {
        $this->loader = new Loader($this->filePath, !$overload);

        return $this->loader->load();
    }
}
```
- `env` 文件变量的读取依赖类 `/Dotenv/Loader` :
```php
class Loader
{
    public function load()
    {
        $this->ensureFileIsReadable();

        $filePath = $this->filePath;
        $lines = $this->readLinesFromFile($filePath);
        foreach ($lines as $line) {
            if (!$this->isComment($line) && $this->looksLikeSetter($line)) {
                $this->setEnvironmentVariable($line);
            }
        }

        return $lines;
    }
}
```
- 我们可以看到，`env` 文件的读取的流程：
```
判断 env 文件是否可读
读取整个 env 文件，并将文件按行存储
循环读取每一行，略过注释
进行环境变量赋值
```
```php
protected function ensureFileIsReadable()
{
    if (!is_readable($this->filePath) || !is_file($this->filePath)) {
        throw new InvalidPathException(sprintf('Unable to read the environment file at %s.', $this->filePath));
    }
}

protected function readLinesFromFile($filePath)
{
    // Read file into an array of lines with auto-detected line endings
    $autodetect = ini_get('auto_detect_line_endings');
    ini_set('auto_detect_line_endings', '1');
    $lines = file($filePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    ini_set('auto_detect_line_endings', $autodetect);

    return $lines;
}

protected function isComment($line)
{
    return strpos(ltrim($line), '#') === 0;
}

protected function looksLikeSetter($line)
{
    return strpos($line, '=') !== false;
}
```
- 环境变量赋值是 `env` 文件加载的核心，主要由 ``setEnvironmentVariable` 函数：
```php
public function setEnvironmentVariable($name, $value = null)
{
    list($name, $value) = $this->normaliseEnvironmentVariable($name, $value);

    if ($this->immutable && $this->getEnvironmentVariable($name) !== null) {
        return;
    }

    if (function_exists('apache_getenv') && function_exists('apache_setenv') && apache_getenv($name)) {
        apache_setenv($name, $value);
    }

    if (function_exists('putenv')) {
        putenv("$name=$value");
    }

    $_ENV[$name] = $value;
    $_SERVER[$name] = $value;
}
```
- `normaliseEnvironmentVariable` 函数用来加载各种类型的环境变量：
```php
protected function normaliseEnvironmentVariable($name, $value)
{
    list($name, $value) = $this->splitCompoundStringIntoParts($name, $value);
    list($name, $value) = $this->sanitiseVariableName($name, $value);
    list($name, $value) = $this->sanitiseVariableValue($name, $value);

    $value = $this->resolveNestedVariables($value);

    return array($name, $value);
}
```
- `splitCompoundStringIntoParts` 用于将赋值语句转化为环境变量名 `name` 和环境变量值 `value`。
```php
protected function splitCompoundStringIntoParts($name, $value)
{
    if (strpos($name, '=') !== false) {
        list($name, $value) = array_map('trim', explode('=', $name, 2));
    }

    return array($name, $value);
}
```
- `sanitiseVariableName` 用于格式化环境变量名：
```php
protected function sanitiseVariableName($name, $value)
{
    $name = trim(str_replace(array('export ', '\'', '"'), '', $name));

    return array($name, $value);
}
```
- `sanitiseVariableValue` 用于格式化环境变量值：
```php
protected function sanitiseVariableValue($name, $value)
{
    $value = trim($value);
    if (!$value) {
        return array($name, $value);
    }

    if ($this->beginsWithAQuote($value)) { // value starts with a quote
        $quote = $value[0];
        $regexPattern = sprintf(
            '/^
            %1$s          # match a quote at the start of the value
            (             # capturing sub-pattern used
             (?:          # we do not need to capture this
              [^%1$s\\\\] # any character other than a quote or backslash
              |\\\\\\\\   # or two backslashes together
              |\\\\%1$s   # or an escaped quote e.g \"
             )*           # as many characters that match the previous rules
            )             # end of the capturing sub-pattern
            %1$s          # and the closing quote
            .*$           # and discard any string after the closing quote
            /mx',
            $quote
        );
        $value = preg_replace($regexPattern, '$1', $value);
        $value = str_replace("\\$quote", $quote, $value);
        $value = str_replace('\\\\', '\\', $value);
    } else {
        $parts = explode(' #', $value, 2);
        $value = trim($parts[0]);

        // Unquoted values cannot contain whitespace
        if (preg_match('/\s+/', $value) > 0) {
            throw new InvalidFileException('Dotenv values containing spaces must be surrounded by quotes.');
        }
    }

    return array($name, trim($value));
}
```
- 这段代码是加载 `env` 文件最复杂的部分，我们详细来说：
```
若环境变量值是具体值，那么仅仅需要分割注释 # 部分，并判断是否存在空格符即可。
若环境变量值由引用构成，那么就需要进行正则匹配，具体的正则表达式为：
```
```javascript
/^"((?:[^"\\]|\\\\|\\"))".*$/mx
```
- 这个正则表达式的意思是：
```
提取 “” 双引号内部的字符串，抛弃双引号之后的字符串
若双引号内部还有双引号，那么以最前面的双引号为提取内容，例如 "dfd("dfd")fdf"，我们只能提取出来最前面的部分 "dfd("
对于内嵌的引用可以使用 \" ，例如 "dfd\"dfd\"fdf",我们就可以提取出来 "dfd\"dfd\"fdf"。
不允许引用中含有 \，但可以使用转义字符 \\
```


- 更多资料：
- https://laravel-china.org/articles/5638/laravel-env-the-loading-of-environment-variables-and-source-code-analysis
