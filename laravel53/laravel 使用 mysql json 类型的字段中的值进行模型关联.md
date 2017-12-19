- 仓库中如下：
```php
/**
	 * @return mixed|ErpReports[]
	 */
	public function getEmployeeList()
	{
		return $this->filter()->select('*', 'fields_json->employee_id as employee_id')->with('hasOneEmployee')->where('type', ErpReports::TYPE_EMPLOYEE)->order()->paginate();
	}
```

- model 中如下：
```php
/**
	 * 属于一个员工
	 * @return \Illuminate\Database\Eloquent\Relations\BelongsTo|\App\Models\Employee\Employee
	 */
	public function hasOneEmployee()
	{
		return $this->belongsTo('App\Models\Employee\Employee', 'employee_id', 'employee_id');
	}
```

