#### java 示例

一句话描述状态模式 
定义功能接口，不同状态下的功能实现，定义状态接口，在controller中通过setState来实现后续不同行为的产生。 

- 功能接口
```
public interface Function {

    void drive();

    void run();

    void back();

}
```
- 功能实现接口1
```
public class OffLineState implements Function {
    @Override
    public void drive() {
        System.out.print("不在线的drive");
    }

    @Override
    public void run() {
        System.out.print("不在线的run");
    }

    @Override
    public void back() {
        System.out.print("不在线的back");
    }
}
```
- 功能实现接口2
```
public class OnLineState implements Function {
    @Override
    public void drive() {
        System.out.print("在线的drive");
    }

    @Override
    public void run() {
        System.out.print("在线的run");
    }

    @Override
    public void back() {
        System.out.print("在线的back");
    }
}
```
- 状态接口
```
public interface State {

    void offLine();
    void onLine();
}
Controller
```
```
public class StateController implements State {

    Function func;

    public void setstate(Function c) {
        this.func = c;
    }


    @Override
    public void offLine() {
        //设置不同的状态
        setstate(new OffLineState());
    }

    @Override
    public void onLine() {
         //设置不同的状态
        setstate(new OnLineState());
    }

    public void drive() {
        func.drive();
    }

    public void run() {
        func.run();
    }

    public void back() {
        func.back();
    }
}
```
- cliet调用
```
  /**
     * 测试状态模式：与策略模式代码形式相似，但是状态模式会影响后续行为
     */
    public void testState() {
        StateController controller = new StateController();
        //设置状态
        controller.onLine();
        //省去了很多if-else的结构
        controller.run();
        controller.drive();
        controller.back();

    }
```
- 优点： State模式将所有与一个特定的状态相关的行为都放进一个状态对象中，他提供了一个更好的方法来组织与特定状态相关的代码，将繁琐的状态判断转换成结构清晰的状态类族，在避免代码膨胀的同事也保证了可扩展性与可维护性。

- 缺点： 增加了系统类和对象的个数。

- http://blog.csdn.net/laner0515/article/details/7383872

- http://blog.csdn.net/ghevinn/article/details/24792071

- http://blog.csdn.net/kai763253075/article/details/52496741
