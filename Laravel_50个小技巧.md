Eloquent

1.Automatic model validation
```php
class Post extends Eloquent
{
    public static $autoValidate = true;
    protected static $rules = array();

    protected static function boot()
    {
        parent::boot();
        // You can also replace this with static::creating or static::updating
        static::saving(function ($model) {
            if($model::$autoValidate) {

                return $model->validate();
            }
        });
    }

    public function validate() { }
}
```

2.Prevent updating

```php
class Post extends Eloquent

{
    protected static function boot()
    {
        parent::boot();
        static::updating(function ($model) {
            return false;
        });
    }
}
```
3.Conditional relationships

```php
class myModel extents Model
{
     public function category()
     {
         return $this->belongsTo('myCategoryModel', 'categories_id')->where('users_id', Auth::user()->id);
     }
}
```
4.Expressive where syntax

```php
$products = Product::where('category', '=', 3)->get();
$products = Product::where('category', 3)->get();
$products = Product::whereCategory(3)->get();
```

5.Query builder:having raw

```php
SELECT *, COUNT(*) FROM products GROUP BY category_id HAVING count(*) > 1;

DB::table('products')
    ->select('*', DB::raw('COUNT(*) as products_count'))
    ->groupBy('category_id')
    ->having('products_count', '>', 1)
    ->get();
Product::groupBy('category_id')->havingRaw('COUNT(*) > 1')->get();

```
6.Simple date filtering
```php
$q->whereDate('created_at', date('Y-m-d'));
$q->whereDay('created_at', date('d'));
$q->whereMonth('created_at', date('m'));
$q->whereYear('created_at', date('Y'));
```
7.Save options

```php
//src/Illuminate/Database/Eloquent/Model.php
public function save(array $options = array());

 //src/Illuminate/Database/Eloquent/Model.php
protected function performUpdate(Builder $query, array $options = [])
{
    if($this->timestamps && array_get($options, 'timestamps', true)) {
        $this->updateTimestamps();
    }


    $product = Product::find($id);
    $product->updated_at = '2015 -01-01 10:00:00';
    $product->save(['timestamps' => false]);
```
8.Multilingual support

```php
// database/migrations/create_articles_table.php
public function up()
{
    Schema::create('articles', function (Blueprint $table) {
        $table->increments('id');
        $table->boolean('online');
        $table->timestamps();
    });
}
```
//database/migrations/create_articles_table.php
```php
public function up()
{
    $table->increments('id');
    $table->integer('article_id')->unsigned();
    $table->string('locale')->index();
    $table->string('name');
    $table->text('text');
    $table->unique(['article_id', 'locale']);
    $table->foreign('article_id')->references('id')->on('articles')->onDelete('cascade');

}
```

// app/Article.php
```php
class Article extends Model
{
    use \Dimsav\Translatable\Translatable;
    public $translatedAttributes = ['name', 'text'];
}
```
// app/ArticleTranslation.php
```php
class ArticleTranslation extends Model
{
    public $timestamps = false;
}
```
// app/http/routes.php
```php
Route::get('{locale}', function ($locale) {
    app()->setLocale($locale);
    $article = Article::first();
    return view('article')->with(compact('article'));
});
```
// resources/views/article.blade.php
```php
<h1>{{ $article->name }}</h1>

{{ $article->text }}
```
9.Retrieve random rows
```php
$questions = Question::orderByRaw('RAND()')->take(10)->get();
```
10.uuid model primary key
```php
use Ramsey\Uuid\Uuid;
 trait UUIDModel
 {
     public $incrementing = false;
     protected static function boot()
     {
         parent::boot();
         static::creating(function ($model) {
             $key = $model->getKeyName();
             if(empty($model->{$key})) {
                 $model->{$key} = (string)$model->generateNewId();
             }
         });
     }

     public function generateNewUuid()
     {
         return Uuid::uuid4();
     }
 }
```
11.Ordered relationships
```php
class Category extends Model
 {
     public function products()
     {
         return $this->hasMany('App\Product')->orderBy('name');
     }
 }
```
12.Simple incrementing & Decrementing
```php
$customer = Customer::find($customer_id);
$loyalty_points = $customer->loyalty_points + 50;
$customer->update(['loyalty_points' => $loyalty_points]);
```
// adds one loyalty point
```php
Customer::find($customer_id)->increment('loyalty_points', 50);
```
// subtracts one loyalty point
```php
Customer::find($customer_id)->decrement('loyalty_points', 50);
```
13.List with mutations
```php
$employees = Employee::where('branch_id', 9)->lists('name', 'id');
return view('customers . create', compact('employees'));

 {!! Form::select('employee_id', $employees, '') !!}

 public function getFullNameAttribute() { 
     return $this->name . ' ' . $this->surname;
 }


 [2015-07-19 21:47:19] local.ERROR: exception 'PDOException' with message 'SQLSTATE[42S22]: Column not found:
 1054 Unknown column 'full_name' in 'field list'' in
 ...vendor\laravel\framework\src\Illuminate\Database\Connection.php:288


$employees = Employee::where('branch_id', 9)->get()->lists('full_name', 'id');
```
14.Appending mutated properties
```php
function getFullNameAttribute()
{
    return $this->first_name . ' ' . $this->last_name;
}


{
    "id":1,
    "first_name":"Povilas", 
    "last_name":"Korop",
    "email":"[email protected]
", "created_at":"2015-06-19 08:16:58", "updated_at":"2015-06-19 19:48:09" } class User extends Model { protected $appends = ['full_name']; { "id":1, "first_name":"Povilas", "last_name":"Korop", "email":" [email protected]
", "created_at":"2015-06-19 08:16:58", "updated_at":"2015-06-19 19:48:09", "full_name":"Povilas Korop" }
```

15.Filter only rows with child rows
```php
class Category extends Model
{
    public function products()
    {
        return $this->hasMany('App\Product');
    }
}

public function getIndex()
{
    $categories = Category::with('products')->has('products')->get();
    return view('categories.index', compact('categories'));
}

```
16.Return relations on model save
```php
public function store()
{
    $post = new Post;
    $post->fill(Input::all());
    $post->user_id = Auth::user()->user_id;
    $post->user;
    return $post->save();
 }
 ```
#### Blade

17.Dynamic with
```php
// eloquent
Post::whereSlug('slug')->get();

// instead of
View::make('posts.index')->with('posts', $posts);

// do this
View::make('posts.index')->withPosts($posts);
18.First/last array element

//hide all but the first item

@foreach ($menu as $item)

<div @if ($item != reset($menu)) class="hidden" @endif>

<h2>{{ $item->title }}</h2>

     </div>

 
@endforeach


 //apply css to last item only

 @foreach ($menu as $item)


<div @if ($item == end($menu)) class="no_margin" @endif> 

<h2>{{ $item->title }}</h2>

 </div>

 
@endforeach
Collections
```
19.Arrays as collections
```php
$devs = [
    ['name' => 'Anouar Abdessalam', 'email' => '[email protected]
'], ['name' => 'Bilal Ararou', 'email' => '[email protected]'] ]; $devs = new Illuminate\Support\Collection($devs); $devs->first(); $devs->last(); $devs->push(['name' => 'xroot', 'email' => ' [email protected]
']);
```
20.Collection filters
```php
$customers = Customer::all();
$us_customers = $customers->filter(function ($customer) {
    return $customer->country == 'United States';
});

$non_uk_customers = $customers->reject(function ($customer) {
    return $customer->country == 'United Kingdom';
});
```
21.find()
```php
//	returns a single row as a collection
$collection = App\Person::find([1]);

//	can return multiple rows as a collection
$collection = App\Person::find([1, 2, 3]);
```
22.where()
```php
$collection = App\Person::all();
$programmers = $collection->where('type', 'programmer');
$critic = $collection->where('type', 'critic');
$engineer = $collection->where('type', 'engineer');
```
23.implode()
```php
$collection = App\Person::all();
$names = $collection->implode('first_name', ',');
```
24.where() & list()
```php
// returns a collection of first names

$collection = App\Person::all()->where('type', 'engineer')->lists('first_name');

// returns all the meta records for user 1
$collection = App\WP_Meta::whereUserId(1)->get();

// returns the first & last name meta values

$first_name = $collection->where('meta_key', 'first_name')->lists('value')[0];
$last_name = $collection->where('meta_key', 'last_name')->lists('value')[0];
```
25.order belongs-to-many by pivot table
```php
class Link extends Model

 {
     public function users()
     {
         return $this->belongsToMany('Phpleaks\User')->withTimestamps();
     }
 }


@if ($link->users->count() > 0)
<strong>Recently Favorited By</strong>
 @foreach ($link->users()->orderBy('link_user.created_at', 'desc')->take(15)->get() as $user)


        <a href="{{ URL::Route('user.show', array('id' => $user->id)) }}">{{ $user->name }}</a>
     

 @endforeach
@endif
26.sorting with closures

$collection = collect([
    ['name' => 'Desk'],
    ['name' => 'Chair'],
    ['name' => 'Bookcase']
]);

$sorted = $collection->sortBy(function ($product, $key) {
    return array_search($product['name'], [1 => 'Bookcase', 2 => 'Desk', 3 => 'Chair']);
});

```
27.keying arrays
```php
$library = $books->keyBy('title');

[
    'Lean Startup' => ['title' => 'Lean Startup', 'price' => 10],
    'The One Thing' => ['title' => 'The One Thing', 'price' => 15],
    'Laravel: Code Bright' => ['title' => 'Laravel: Code Bright', 'price' => 20],
    'The 4-Hour Work Week' => ['title' => 'The 4-Hour Work Week', 'price' => 5],
]
```
28.grouped collections
```php
$collection = App\Person::all();
$grouped = $collection->groupBy('type');
```
29.collection unions
```php
// the point is to actually combine results from different models
$programmers = \App\Person::where('type', 'programmer')->get();
$critic = \App\Person::where('type', 'critic')->get();
$engineer = \App\Person::where('type', 'engineer')->get();

$collection = new Collection;

$all = $collection->merge($programmers)->merge($critic)->merge($engineer);
```
30.collection lookaheads
```php
$collection = collect([1 => 11, 5 => 13, 12 => 14, 21 => 15])->getCachingIterator();
foreach ($collection as $key => $value) {
    dump($collection->current() . ':' . $collection->getInnerIterator()->current());
}
Routing
```
31.nested route groups
```php
Route::group(['prefix' => 'account', 'as' => 'account.'], function () {

    Route::get('login', ['as' => 'login', 'uses' => 'AccountController@getLogin']);
    Route::get('register', ['as' => 'register', 'uses' => 'AccountController@getRegister']);

    Route::group(['middleware' => 'auth'], function () {
        Route::get('edit', ['as' => 'edit', 'uses' => 'AccountController@getEdit']);
    });

});

<a href="{{ route('account.login') }}">Login</a>
<a href="{{ route('account.register') }}">Register</a>
<a href="{{ route('account.edit') }}">Edit Account</a>
```
32.catch-all view route
```php
// app/Http/routes.php

Route::group(['middleware' => 'auth'], function () {
    Route::get('{view}', function ($view) {
        try {
            return view($view);
        } catch (\Exception $e) {
            abort(404);
        }
    })->where('view', '.*');
});
```
33.internal dispatch
```php
// api controller

public function show(Car $car)
{
    if(Input::has('fields')) {
        // do something
    }
}

// internal request to api - fields are lost

$request = Request::create('/api/cars/' . $id . '?fields=id,color', 'GET');
$response = json_decode(Route::dispatch($request)->getContent());

// internal request to api - with fields $originalInput = Request::input();

$request = Request::create('/api/cars/' . $id . '?fields=id,color', 'GET');
Request::replace($request->input());
$response = json_decode(Route::dispatch($request)->getContent());
Request::replace($originalInput);
Testing
```
34.evironmental varlables
```php
// phpunit.xml

<php>
    <env name="APP_ENV" value="testing"/>
    <env name="CACHE_DRIVER" value="array"/>
    <env name="SESSION_DRIVER" value="array"/>
    <env name="QUEUE_DRIVER" value="sync"/>
    <env name="DB_DATABASE" value=":memory:"/>
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="TWILIO_FROM_NUMBER" value="+15005550006"/>
</php>


//	.env.test – add to .gitignore
TWILIO_ACCOUNT_SID = fillmein
TWILIO_ACCOUNT_TOKEN = fillmein


//	access directly from your tests using helper function
env('TWILIO_ACCOUNT_TOKEN');


 // tests/TestCase.php <?php class TestCase extends Illuminate\Foundation\Testing\TestCase { /** * The base URL to use while testing the application. * * @var string */ protected $baseUrl = 'http://localhost'; /** * Creates the application. * * @return \Illuminate\Foundation\Application */ public function createApplication() { $app = require __DIR__ . '/../bootstrap/app.php'; if(file_exists(dirname(__DIR__) . '/.env.test')) { Dotenv::load(dirname(__DIR__), '.env.test'); } $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
         return $app;
     }
 }
```
35.run tests automatically
```php
// gulpfile.js

 var elixir = require('laravel-elixir');

 mix.phpUnit();

 $ gulp tdd
36.share cookie between domains

// app/Http/Middleware/EncryptCookies.php
protected $except = [
    'shared_cookie'

];

Cookie::queue('shared_cookie', 'my_shared_value', 10080, null, '.example.com');
```
37.Easy model & migrations stubs
```bash
$ artisan make:model Books -m
```
38.add spark to existing project
```bash
$ composer require genealabs/laravel-sparkinstaller --dev

 Laravel\Spark\Providers\SparkServiceProvider::class, GeneaLabs\LaravelSparkInstaller\Providers\LaravelSparkInstallerServiceProvider::class,

 //	do not run php artisan spark:install
 $ php artisan spark:upgrade

 //	backup /resources/views/home.blade.php or it will be overwritten
 $ php artisan vendor:publish --tag=spark-full
 ```
39.customize the default error page
```php
namespace App\Exceptions;
use Exception;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Symfony\Component\Debug\ExceptionHandler as SymfonyDisplayer;
class Handler extends ExceptionHandler {
  protected function convertExceptionToResponse(Exception $e) {
    $debug = config('app.debug', false);
    if($debug) {
      return (new SymfonyDisplayer($debug))->createResponse($e);
      
    }
    return response()->view('errors.default', ['exception' => $e], 500);
  }
}
```
40.conditional service providers
```php
// app/Providers/AppServiceProvider.php
public function register()
{
    $this->app->bind('Illuminate\Contracts\Auth\Registrar', 'App\Services\Registrar');

    if($this->app->environment('production')) {
        $this->app->register('App\Providers\ProductionErrorHandlerServiceProvider');
    } else {
        $this->app->register('App\Providers\VerboseErrorHandlerServiceProvider');
    }
}
```
43.extending the application
```php
//	bootstrap/app.php

//	replace this:
$app = new Illuminate\Foundation\Application(realpath(__DIR__ . '/../'));

// with this:
$app = new Fantabulous\Application(realpath(__DIR__ . '/../'));

<?php
namespace Fantabulous;
class Application extends \Illuminate\Foundation\Application { 
/** 
* Get the path to the storage directory. 
* @return string 
*/
  public function storagePath() {
    return $this->basePath . '/FantabulousStorage';

  }
}
```
44.simple chching microservice
```php
class fakeApiCaller
 {
     public function getResultsForPath($path)
     {
         return [
             'status' => 200,
             'body' => json_encode([
                 'title' => "Results for path [$path]"
             ]),
             'headers' => [
                 "Content-Type" => "application/json"
             ]
         ];
     }
 }

 $app->get('{path?}', function ($path) {
     $result = Cache::remember($path, 60, function () use ($path) {
         return (new fakeApiCaller)->getResultsForPath($path);
     });

     return response($result['body'], $result['status'], array_only($result['headers'], [
             'Content-Type',
             'X-Pagination'
         ]));
 })->where('path', '.*');
 ```
45.use bleeding edge version
```php
$ composer create - project laravel / laravel your-project-name-here dev-develop

 // composer.json
 {
     "require": {
     "php": ">=5.5.9", "laravel/framework": "5.2.*"
    },
    "minimum-stability": "dev"
 }

$ composer update
```
46.capture queries
```php
Event::listen('illuminate.query', function ($query) {
    var_dump($query);

});


\DB::listen(function ($query, $bindings, $time) {
    var_dump($query);

    var_dump($bindings);
    var_dump($time);

});
```
47.authorization without models
```php
//	app/Policies/AdminPolicy.php
class AdminPolicy
{
    public function managePages($user)
    {
        return $user->hasRole(['Administrator', 'Content Editor']);
    }
}

//	app/Providers/AuthServiceProvider.php

public function boot(\Illuminate\Contracts\Auth\Access\GateContract $gate)
{
    foreach (get_class_methods(new \App\Policies\AdminPolicy) as $method) {
        $gate->define($method, "App\Policies\AdminPolicy@{$method}");
    }
    $this->registerPolicies($gate);
}


$this->authorize('managePages'); // in Controllers
@can('managePages') // in Blade Templates
$user->can('managePages'); // via Eloquent
```
48.efficient file transfer with streams
```php
$disk = Storage::disk('s3');

$disk->put($targetFile, file_get_contents($sourceFile));

$disk = Storage::disk('s3');
$disk->put($targetFile, fopen($sourceFile, 'r+'));

$disk = Storage::disk('s3');

$stream = $disk->getDriver()->readStream($sourceFileOnS3);
file_put_contents($targetFile, stream_get_contents($stream), FILE_APPEND);

$stream = Storage::disk('s3')->getDriver()->readStream($sourceFile);
Storage::disk('sftp')->put($targetFile, $stream)
```
49.avoid overflowing log files
```php
$schedule->call(function () {
    Storage::delete($logfile);
})->weekly();
```
50.pipeling
```php
$result = (new Illuminate\Pipeline\Pipeline($container)
    ->send($something)
    ->through('ClassOne', 'ClassTwo', 'ClassThree')
    ->then(function ($something) {
        return 'foo';
    });
```
51.command handler dispatch
```php
class PurchasePodcastCommand extends Command
{
    public $user;
    public $podcast;
    public function __construct(User $user, Podcast $podcast)
    {
        $this->user = $user;
        $this->podcast = $podcast;
    }
}

class PurchasePodcastCommandHandler
{
    public function handle(BillingGateway $billing)
    {
        // Handle the logic to purchase the podcast...

        event(new PodcastWasPurchased($this->user, $this->podcast));
    }
}

class PodcastController extends Controller
{
    public function purchasePodcastCommand($podcastId)
    {
        $this->dispatch(
            new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
        );
    }
}
```
52.self handling commands
```php
class PurchasePodcast extends Command implements SelfHandling
{
    protected $user;
    protected $podcast;

    public function __construct(User $user, Podcast $podcast)
    {
        $this->user = $user;
        $this->podcast = $podcast;
    }

    public function handle(BillingGateway $billing)
    {
        // Handle the logic to purchase the podcast...

        event(new PodcastWasPurchased($this->user, $this->podcast));
    }

}

class PodcastController extends Controller
{
    public function purchasePodcast($podcastId)
    {
        $this->dispatch(
            new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
        );
    }
}
```
53.automatic dispatch from requests
```php
class PodcastController extends Controller
{
    public function purchasePodcast(PurchasePodcastRequest $request)
    {
        $this->dispatchFrom('Fantabulous\Commands\PurchasePodcastCommand', $request);
    }

}


class PodcastController extends Controller
{
    public function purchasePodcast(PurchasePodcastRequest $request)
    {
        $this->dispatchFrom('Fantabulous\Commands\PurchasePodcastCommand', $request, [
            'firstName' => 'Taylor',
        ]);
    }
}
```
54.queued commands
```php
class PurchasePodcast extends Command implements ShouldBeQueued, SerializesModels
{
    public $user;
    public $podcast;

    public function __construct(User $user, Podcast $podcast)
    {
        $this->user = $user;
        $this->podcast = $podcast;
    }
}
```
55.commands pipeline
```php
// App\Providers\BusServiceProvider::boot
$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

class UseDatabaseTransactions
{
    public function handle($command, $next)
    {
        return DB::transaction(function () use ($command, $next) {
            return $next($command);
        });
    }
}


// App\Providers\BusServiceProvider::boot
$dispatcher->pipeThrough([
    function ($command, $next) {
        return DB::transaction(function () use ($command, $next) {
            return $next($command);
        });
    }
]);
Laravel 5.2
```
56.implicit model binding
```php
// app/http/routes.php

Route::get('/api/posts/{post}', function (Post $post) {
    return $post;
});

// behind the scenes
Post::findOrFail($post);
```
57.append scheduler autput to a file
```php
$schedule->command('emails:send')->hourly()->appendOutputTo($filePath);
```
58.collections wildcard
```php
// returns titles for all posts

$titles = $posts->pluck(‘posts .*.title’);
```
59.formarray validation
```php
<input type="text" name="person[1][id]">
<input type="text" name="person[1][name]">
<input type="text" name="person[2][id]"> <input type="text" name="person[2][name]">

$v = Validator:: make($request->all(), [
    'person.*.id' => 'exists:users.id',
    'person.*.name' => 'required:string',

]);
```
60.easily clear user sessions
```php
// included in database session driver
user_id
ip_address
```
