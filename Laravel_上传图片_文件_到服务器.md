#### Laravel 上传图片/文件到服务器

```php
public function upload(Request $rq){
        $postFile = $rq->file('file');
        //获取文件名称
        $clientName = $postFile->getClientOriginalName();
        $realPath = $postFile->getRealPath();
        //获取图片格式
        $entension = $postFile->getClientOriginalExtension();
        //图片保存路径
        $mimeTye = $postFile->getMimeType();
        $newName = base64_encode(rand(10000000,999999999)).'.'.$entension;
        $path = $postFile->move('./uploads/xxxx/'.date('Ymd'), $newName);
        $data = [
            'new_name' => 'uploads/tech/'.$newName
        ];
        return $this->success($data, '上传成功');
}
```
