# record of GPIO-LED part.


## first trial&basic operations

[GPIO-zero docs](https://gpiozero.readthedocs.io/en/stable/recipes.html#led-with-variable-brightness)

```bash
# gpio pin name
gpio readall
gpio mode {PIN} {MODE(output,input)}
gpio read {PIN}
gpio write {PIN} {VALUE(0,1)}
```


```python
import gpiozero

led = gpiozero.LED(26)
led.on()
led.off()
led.toggle()
led.blink(interval_on,interval_off)

# source/value: data-binding, siginal-slot

# PWM
```


by default, gpiozero use BCM pin number  
alternative: `LED("GPIO25"),LED("BCM17"),LED("BOARD1"),LED("WPI0")`,  
remember to run `gpio readall`

## the "bread-board"




