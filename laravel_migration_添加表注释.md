#### 示例：
```php

<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

class CreateStagesBackFullCashTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        $tableName = 'stages_back_full_cash';
        Schema::create($tableName, function (Blueprint $table) {
            $table->engine = 'InnoDB';
            $table->increments('back_full_cash_id');
            $table->integer('user_id')->default(0)->unsigned()->comment('用户ID');
            $table->bigInteger('business_order_id')->default(0)->unsigned()->comment('业务订单ID');
            $table->smallInteger('nper')->default(0)->unsigned()->comment('总期数');
            $table->smallInteger('current_nper')->default(0)->unsigned()->comment('当前期数');
            $table->tinyInteger('status')->default(0)->comment('返还状态 0：未结束 , 1：已结束；');
            $table->integer('start_at')->default(0)->unsigned()->comment('开始返还的时间，确认收货以后会设置这个时间');
            $table->integer('created_at')->default(0)->unsigned()->comment('创建时间');
            $table->integer('updated_at')->default(0)->unsigned()->comment('更新时间');
        });

        DB::statement("ALTER TABLE `$tableName` comment '全额返现_分期返还表'");
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('stages_back_full_cash');
    }
}

```

#### 主要代码：

```php 
use Illuminate\Support\Facades\DB;

...

public function up(){
  ...
  DB::statement("ALTER TABLE `$tableName` comment '全额返现_分期返还表'");
}

...
```
