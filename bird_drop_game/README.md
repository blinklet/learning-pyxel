% Making games using Python and Pyxel

I wrote this tutorial for people who are learning Python and are now ready to explore new concepts like object-oriented programming and Python classes. I assume the reader has already learned the [basics of Python programming](https://www.brianlinkletter.com/2020/09/python-the-minimum-you-need-to-know/).

I think that we learn best when working on a practical project. This tutorial will show readers how to build a simple game that they can share with their friends. While building the game, I will introduce the Pyxel game framework and will use Python classes to build and manage multiple game elements.

# Python Classes

A [Python class](https://docs.python.org/3/tutorial/classes.html) is a new type of Python object used in [object-oriented programming](https://www.freecodecamp.org/news/object-oriented-programming-in-python/). Programmers create instances of classes, by [instantiating](https://realpython.com/python-class-constructor/) a class, and then use or modify those instances' attributes in their programs. 

Each instance of a class is a unique object that may contain data, called attributes, and functions, called methods. 

Each class also contains an initialization function, called a constructor, that runs when a new instance is created. The constructor defines the initial state of the instance, based on code defined in it and any data that may be passed into the instance, when it is created.

To demonstrate the simple use of Python classes, you will build a game using Python and the Pyxel framework. You will use Python classes and learn [fundamental object-oriented programming concepts](https://realpython.com/python3-object-oriented-programming/) such as inheritance[^1]. 

[^1]: I ignore more complex object-oriented concepts such as [composition and interfaces](https://realpython.com/inheritance-composition-python/). Object inheritance is suitable for simple-to-intermediate complexity programs and is relatively easier to understand. It is also the correct way to manage objects in the game we will create because each subclass we create has an "is a" relationship to the parent class.



# The Pyxel Framework

[Pyxel](https://github.com/kitao/pyxel#) is a retro game engine for Python. I chose Pyxel for this tutorial because it is simpler than other game frameworks so you can learn enough about it in a short period of time to start building a simple game.

Pyxel makes it easier for programmers to develop pixel-based games that remind you of old games from the 1980s and 1990s. Pyxel provides a set of functions that do most of the work of managing the game loop, displaying graphics, and playing sounds. Pyxel also offers the Pyxel Editor: an all-in-one solution for creating sprites, tiles, tile maps, sounds, and music for Pyxel games.

The [Pyxel web page](https://github.com/kitao/pyxel#) contains everything you need to know about using Pyxel and the Pyxel Editor. The Pyxel framework is relatively simple and the documentation is compact and clear.

> Please stop here and read the [Pyxel documentation](https://github.com/kitao/pyxel#). Then, continue with this tutorial. It will take about ten minutes to read the documentation.

After that, if you would like to spend some more time learning about Pyxel before or after proceeding with the tutorial, you may look at the following resources:

* Work through the [official Pyxel examples](https://github.com/kitao/pyxel#try-pyxel-examples). Pyxel's developer, [Takashi Kitao](https://twitter.com/kitao), [recommends](https://discord.com/channels/697925198992900106/697925198992900109/930086207239622666) working through the Pyxel examples in the following order: 1, 5, 3, 4, 2, 9, and 10.
* [CaffeinatedTech](https://twitter.com/CaffeinatedTech) produced a [2-hour video walking through the basics of Pyxel](https://youtu.be/Qg16VhEo2Qs) while building a snake game.
* [Emanoel Barreiros](https://twitter.com/ebarreiros) wrote an excellent blog with nine [posts about using Pyxel](https://emanoelbarreiros.github.io/game/snake/snake-1/). The first post is in English and the remaining are in Portuguese but you can [translate](https://kinsta.com/blog/how-to-translate-a-website/) them in your web browser.

If you find you enjoy working with Pyxel, you may wish to join the Pyxel community on the [Pyxel Discord server](https://discord.com/channels/697925198992900106/697925198992900109), where you can find information and inspiration.

# Install Pyxel and create environment

To work with Pyxel and follow the examples in this post, first create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) and install Pyxel in that environment. Then, install the Pyxel example files so you can re-use some of the assets from the examples in this tutorial. Execute the following commands [^2]:

[^2]: I use a PC running Linux in all the examples. If you are using a Mac or a PC, you will use [slightly different commands](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) to launch Python or to activate a Python virtual environment

```bash
$ mkdir learn_pyxel
$ cd learn_pyxel
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install pyxel
$ pyxel copy examples 
```

List the contents of the *learn_pyxel* directory:

```bash
$ ls
env  pyxel_examples
```

The game resources you will use in this tutorial are stored in the *pyxel_examples/assets* directory:

```bash
$ ls -1 pyxel_examples/assets
cat_16x16.png
jump_game.pyxres
noguchi_128x128.png
offscreen.pyxres
platformer.pyxres
pyxel_logo_38x16.png
sample.pyxres
tileset_24x32.png
```

In all the examples below, we will use the assets in the *platformer.pyxres* file because it contains a simple set of sprites. 

Create a new folder for your first game project and copy the resource file into your project folder:

```bash
$ mkdir first_game
$ cp pyxel_examples/assets/platformer.pyxres first_game
$ cd first_game
```

You can view the resource file in the Pyxel resource editor using the following Pyxel command:

```bash
$ pyxel edit platformer.pyxres
```

You should see a new window appear on your desktop that looks like the image below:

![](./Images/pyxel_editor_1.png)

This is the [Pyxel Editor](https://github.com/kitao/pyxel#how-to-create-resources). You may use it to view and create sprites, tiles, tile maps, sounds, and music for Pyxel games. 

In these tutorials, we focus on Python programming and using Python classes so we will not cover how to create new assets in the Pyxel resource editor. In this tutorial, you will use the Pyxel Editor to find existing game assets in existing resource files. See the [2-hour video walking through the basics of Pyxel](https://youtu.be/Qg16VhEo2Qs) I previously referenced if you want a good introduction to creating new assets in the Pyxel Editor. 

Quit the editor by pressing the *Escape* key.

# First Pyxel program

Create a small Pyxel program that displays an animation of a bird flapping its wings. In this example, write the program in the procedural style so we can contrast this version to a program written in the object-oriented style, later.

Re-use the bird sprites in the resource file *platformer.pyxres* from the [Pyxel examples](https://github.com/kitao/pyxel#try-pyxel-examples) you downloaded. The three bird sprites are on *Image 0* and are in (x, y) positions (0, 16), (8, 16), and (16, 16). Each sprite is eight pixels high, eight pixels wide, and shows the bird in a different animated position.

First, import the *pyxel* module, initialize the screen size and frame rate (per second), and load the Pyxel resource file *platformer.pyxres*:

```python
import pyxel

pyxel.init(64, 32, fps=2)
pyxel.load("platformer.pyxres")
```

Next, create the *update* and *draw* functions required by the Pyxel framework and pass them into the *pyxel.run* function, which manages the game loop:

```python
def update():
    pass

def draw():
    pass

pyxel.run(update, draw)
```

If you were to save and run this program right now, you would see a new window is created that is twice as wide as it is tall. The window contains nothing because we did not define anything in the *draw* function.

Quit the program by pressing the *Escape* key.

To display one of the bird sprites, change the draw function to the following:

```python
def draw():
    pyxel.cls(6)
    pyxel.blt(28, 12, 0, 0, 16, 8, 8)
```

See the [Pyxel Graphics documentation](https://github.com/kitao/pyxel#graphics) for a description of the *pyxel.cls* function, which clears the screen and replaces everything with a specified color, and the *pyxel.blt* function, which copies a defined bitmap area from the resource file and places is in the Pyxel game screen. If you save and run the program now, you will see the eight-by-eight pyxel bird sprite appears on the screen. This sprite was copied from an eight-by-eight pixel area starting at x and y coordinates 0 and 16 in the resource file's Image 0. On the game screen, the upper right corner of the sprite is placed at x and y coordinates of 28 and 12 on the screen, making it appear like the bird is centered in the screen.

The *pyxel.blt* function has an optional parameter that lets you specify a transparent color on the sprite so it looks better on various backgrounds. In this case, the sprite's background color is [color number 2](https://github.com/kitao/pyxel#color-palette). Add that parameter to the *pyxel.blt* function, as shown below:

```python
def draw():
    pyxel.cls(6)
    pyxel.blt(28, 12, 0, 0, 16, 8, 8, 2)
```

If you save and run the program now, you will see a window similar to the one below:

![](./Images/pyxel_bird_1.png)

Now, animate the bird by changing which sprite image is displayed in each frame. Since the three bird sprites are all in a line whose top edge is 16 pixels down from the top if Image 0 in the Pyxel resource file, we just to change the value for the x-position of each sprite in the *pyxel.blt* function.

The usual place to store logic that updates the positions or properties of game elements is the *update* function.

Change the *update* function to the following:

```python
def update():
    sprite_u = 8 * (pyxel.frame_count % 3)
```

The *pyxel.frame_count* increments by one each time Pyxel runs through the game loop. The [modulo operator](https://datagy.io/python-modulo/) leaves the remainder of division so will result in a value of 0, 1, or 2 depending on the frame count. Multiply that by eight and you get a *sprite_u* value of 0, 8, or 16 depending on the frame.

Replace the sprite hard-coded x value in *pyxel.blt* function in the *play* function with the *sprite_u* variable.

```python
def draw():
    pyxel.cls(6)
    pyxel.blt(28, 12, 0, sprite_u, 16, 8, 8, 2)
```

When you save and run the program, you see the first problem you need to solve: Python stops the program with an error because the variable *sprite_u* is not available outside the scope of the *update* and *draw* functions.

One way to solve this is to use global variables, which are accessible in the local [namespace](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces) of any function that declares them. 

Below, I declared the `sprite_u` variable as a global variable in both functions. This solves the problem, for now, but will get hard to manage as the program gets more complex. Generally, programmers do not want to use global variables to store program state.

Change the *update* and *draw* functions as shown below:

```python
def update():
    global sprite_u
    sprite_u = 8 * (pyxel.frame_count % 3)

def draw():
    global sprite_u
    pyxel.cls(6)
    pyxel.blt(28, 12, 0, sprite_u, 16, 8, 8, 2)
```

Now the program runs, the variable *sprite_u* can be assigned in the *update* function and its value can be read in the *draw* function.

But, the animation is too fast. We could reduce the animation speed by lowering the frame rate but that is not a good solution for the project because it will impact the future versions of the game. 

Managing the speed of game elements relative to the game frame rate is one of the first problems you need to solve in game development. As you add more elements, with different movement speeds and animation speeds, you need a way to control how often a piece of code executes relative to the game's frame rate.

One solution is to create yet another global variable that tracks the sprite frame index. Increment the frame index once every ten frames. When the frame index has incremented to 3, reset it to zero so it can continue to be used to calculate the sprite animations. For example:

```python
animation_index = 0

def update():
    global sprite_u
    global animation_index
    if pyxel.frame_count % 10 == 0:
        if animation_index > 2:
            animation_index = 0
        sprite_u = 8 * animation_index
        animation_index += 1
```

Note that you had to assign a value to the *animation_index* variable in the main body of the program because you must assign a Python variable before you use it. This is OK because, after it the variable is initially assigned, that initialization code does not run again. The Pyxel framework only runs code that is inside the *update* and *draw* functions during the game.

After you save and run the program, the *sprite_u* variable iterates between 0, 8, 16, and back to 0 every ten frames, or third of a second.

![](./Images/bird_animation_1.gif)

You will use this algorithm multiple times when you have different sprites moving at different speeds. You can imagine how complex it will get if you have to manage it with global variables.

# Pyxel program using classes

In many cases, Python classes make it easier to organize and use data in your program. This is evident when we compare the examples above, written in a procedural style, with the examples below, written in an object-oriented style.

The Pyxel documentation [recommends that you wrap pyxel code in a class](https://github.com/kitao/pyxel#create-pyxel-application) so developers can avoid using global variables to pass data from the `update()` function to the `draw()` function in a Pyxel program. If the Pyxel code is wrapped in a class, one can store data in the object instance created when the class is called. That data can be accessed by the rest of the program.

Refactor the first Pyxel program you previously wrote into an program that places the program logic in a class named *App*. See the example below:

```python
import pyxel

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.animation_index = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count % 10 == 0:
            if self.animation_index > 2:
                self.animation_index = 0
            self.sprite_u = 8 * self.animation_index
            self.animation_index += 1

    def draw(self):
        pyxel.cls(6)
        pyxel.blt(28, 12, 0, self.sprite_u, 16, 8, 8, 2)

App()
```

You defined a class named *App*. In it, you defined the *constructor* method, named *__init__*, which [initializes an instance](https://docs.python.org/3/tutorial/classes.html#class-objects) of the *App* class in a known state. Since the class does not have any parameters, other than the *self* parameter, the initial state will be the same in every time the class is called, or instantiated. The program calls the class when it is run.

The [*self* parameter](https://www.digitalocean.com/community/tutorials/how-to-construct-classes-and-define-objects-in-python-3) represents the instance of the class that will be created when it is instantiated, or called. This object is passed into every method in the class so that all variables in the class are accessible to all the class's methods, such as the *update* and *draw* methods. This eliminates the need for global variables because all variables are now attributes of the *self* object.

Another benefit of using classes is realized when you create multiple instances of the same class. For example, you can define a *Sprite* class, which separates all the logic and data associated with the bird sprites from the main program, and create multiple instances of birds on the screen, each with its own position data.

```python
import pyxel

class Sprite:
    def __init__(self, x, y, index):
        self.sprite_x = x
        self.sprite_y = y
        self.animation_index = index

    def update(self):
        if pyxel.frame_count % 10 == 0:
            if self.animation_index > 2:
                self.animation_index = 0
            self.sprite_u = 8 * self.animation_index
            self.animation_index += 1

    def draw(self):
        pyxel.blt(self.sprite_x, self.sprite_y, 0, self.sprite_u, 16, 8, 8, 2)
```

The *App* class is now simplified because it does not need to manage the state of each bird sprite. You are beginning to see the benefits of *information hiding*, which we will discuss more later. When the *App* class is called, it's initialization method instantiates two bird sprite objects by twice calling the *Sprite* class with different parameters. Then we just call the bird sprite objects' *update* and *draw* methods in the *App* class during each game loop cycle, or frame.

```python
class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.bird1 = Sprite(6,6,0)
        self.bird2 = Sprite(28,12,1)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.bird1.update()
        self.bird2.update()

    def draw(self):
        pyxel.cls(6)
        self.bird1.draw()
        self.bird2.draw()

App()
```

You see in the example above, each bird object is initialized with data parameters representing its *x* and *y* coordinates on the game screen, and the animation index. When you run the program, you see two birds on the screen in different locations, with each bird seeming to flap it's wings at different times because each bird starts its animation sequence at a different frame set by the animation index.. 

You can easily add yet another bird, with its own position and animation index, with just one line of code in each of the *App* class's *update* and *draw* methods. You could add a *for* loop that creates hundreds of bird sprites and saves them in a list. Then, you could update and draw those sprites by iterating through the sprite list in each of the *update* and *draw* methods. 

We could further extend the *Sprite* class to include methods that change its position on the screen as time passes and to detect and respond to other game elements. All the information about position, speed, animation is managed separately by each instance of the *Sprite* class so it is possible to manage many birds in the same program.

For example, if we change the *App* class as shown below, we can generate a dozen bird sprites in random locations on the screen:

```python
class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.sprite_list = []
        for i in range(12):
            a = pyxel.rndi(0,56)
            b = pyxel.rndi(0,24)
            c = pyxel.rndi(0,2)
            self.sprite_list.append(Sprite(a, b, c))
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()
```

Running the program shows twelve bird sprites in random locations around the screen, all flapping their wings independently.

Defining the bird sprite state in the *Sprite* class allows us to change the behavior of the bird sprites instantiated from that class without changing the rest of the. For example, if we change the *Sprite* class to make the bird sprites move one pixel in a random direction every ten frame, we change the *Sprite* class to the following:

```python
class Sprite:
    def __init__(self, x, y, index):
        self.sprite_x = x
        self.sprite_y = y
        self.animation_index = index

    def move(self):
        self.sprite_x += pyxel.rndi(-1,1)
        self.sprite_y += pyxel.rndi(-1,1)
    
    def animate(self):
        if self.animation_index > 2:
            self.animation_index = 0
        self.sprite_u = 8 * self.animation_index
        self.animation_index += 1

    def update(self):
        if pyxel.frame_count % 10 == 0:
            self.animate()
            self.move() 

    def draw(self):
        pyxel.blt(self.sprite_x, self.sprite_y, 0, self.sprite_u, 16, 8, 8, 2)
```

In this case, you added a *move* method that changes the bird sprite's x and y coordinates by one pixel in some random direction. Then you moved the sprite animation code from the *update* method into its own *animate* method. Finally, you called the *animate* and *move* methods in the modified *update* method.

You did not need to modify the main application class, *App*, to change the behavior of all the bird sprites. You may be starting to see how Python classes and object-oriented programming enable programmers to build objects that can hide information from each other so that the code in one object does not need to know about all the code in another object. 

# Information hiding

[Information-hiding](https://en.wikipedia.org/wiki/Information_hiding) makes it easier for multiple programmers to work together on the same project.

*Information hiding* is also called *encapsulation*. It is usually accomplished by breaking a large program up into smaller files, called modules. Programmers who are working together agree on how code in one module can access code in another module. This agreement is called an *interface*. As long as you do not change a module's interface, you can add or change the rest of the code to improve the functionality of your module, without negatively impacting the functionality of your colleagues' code. 

For example, you can split your current program into two files, or modules, named *sprites.py* and *game.py* where the *sprites.py* file contains all the code for the *Sprite* class, and the *game.py* file contains all the main program code, including the Pyxel *App* class. 

To make it clear how we can limit what the main program needs to know about each sprite, modify the code in each file so that all the logic related to positioning and animating the sprites is in the *Sprite* class in the *sprites.py* module and the main game logic is simplified to just instantiating new sprite objects and calling each sprite's *update* and *draw* methods during the game loop.

Modify the *game.py* file so it looks like the following. First, you need to import the Sprite class from the *sprites.py* module. Then, simplify the *App* class* so it no longer needs to know the position and animation index of each sprite. In it's constructor, the *App* object instantiates new sprites simply by calling the *Sprite* class and appending the returned sprite objects to a list. All the code that randomly assigns position and animation index will be encapsulated inside the *Sprite* class and the actual values for those attributes, which are different for each sprite object, will be managed and updated within each sprite object.

```python
import pyxel
from sprites import Sprite

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.sprite_list = []
        for _ in range(12):
            self.sprite_list.append(Sprite())
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()
```

Now, whomever maintains the *game.py* file can concentrate on adding and removing sprites and adding game features like different screens or interesting backgrounds and can leave the work of improving sprite animation and movement to another programmer who maintains the *sprites* module.

Modify the code in the *sprites.py* module so that it no longer accepts parameters. Add to the *Sprite* class's controctor method the code that assigns the initial position and animation index. To make the *sprite* class more customizable, I added separate timers for animation and movement and expressed the timer values as variables, which become object attributes when the constructor runs, instead of hard-coded numbers.

Also, generalize the animation logic so that we no longer need animations to be across the same line in the Pyxel resource file. Define the animation sequence as a set up x and y coordinates pointing to upper right corner of each sprite in the animation. Assign the sprite width and height to variables in the constructor. This will make is possible for programmers who use the Sprite class to customize it in their game program.

```python
import pyxel

class Sprite:
    def __init__(self):
        self.x = pyxel.rndi(0,56)
        self.y = pyxel.rndi(0,24)
        self.w = 8
        self.h = 8
        self.col = 2
        self.animate_interval = 10
        self.move_interval = 25
        self.animation = ((16, 16), (0, 16), (8, 16), (0, 16))
        self.animation_index = pyxel.rndi(0,len(self.animation))

    def move(self):
        if pyxel.frame_count % self.move_interval == 0:
            self.x += pyxel.rndi(-1,1)
            self.y += pyxel.rndi(-1,1)
    
    def animate(self):
        if pyxel.frame_count % self.animate_interval == 0:
            if self.animation_index == len(self.animation):
                self.animation_index = 0
            self.u, self.v = self.animation[self.animation_index]
            self.animation_index += 1

    def update(self):
        self.animate()
        self.move() 

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, self.col)
```

When you run the *game.py* program you will see the same result as before: twelve bird sprites animating and moving around on the screen. 

# Inheritance

[Inheritance](https://www.digitalocean.com/community/tutorials/understanding-class-inheritance-in-python-3) is an object-oriented programming feature that enables you to add new types of sprites to your game program without modifying any code in the *sprites.py* file. You can build new classes based on existing classes where you *inherit* all the functionality of the base class and then add new code that changes some of the base class' attributes or methods in the new class.'

For example, in the game program, Add a new type of sprite taht looks like an ball that flashes different colors. Open the Pyxel resource file and find the three different-colored ball sprites:

```bash
$ pyxel edit platformer.pyxres
```

See that each ball sprite is six pixels wide and six pixels high, and that the green ball sprite is located at coordinates (1, 9), the red ball is located at coordinates (9, 9), and the yellow ball sprite is located at coordinates (17, 9). Quit the Pyxel Edit program and use the information you gathered to build a new sprite type.

You do not need to write a whole new class for the ball sprite. Build the new *Ball* class by inheriting all the attributes and methods from the *Sprite* class and then just change the sprite width, height, and animation sequence information in the *Ball* class constructor. See the code below, which creates the new class:

```python
class Egg(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 6
        self.h = 6
        self.animation = ((1, 9), (9, 9), (17, 9))
        self.animation_index = pyxel.rndi(0,len(self.animation))
```

You *inherit* the base class's functionality by calling the [super class's constructor method](https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods/27134600#27134600) in the new class's constructor. The super function just provides a [general-purpose way to call the parent class's constructor method](https://realpython.com/python-super/) and is recommended practice instead of "hard coding" the Sprite class's constructor with a statement like: `Sprite.__init__(self)`.


Insert the above code before the *App* class in the *game.py* file. The modify the *App* class constructor so it addes both ball sprites and normal bird sprites to the sprite list. Change the sprite list creation loop in the *App* class constructor to the following, which creates a list with twelve elements: six birds and six balls.

```python
        self.sprite_list = []
        for _ in range(6):
            self.sprite_list.append(Sprite())
            self.sprite_list.append(Ball())
```

The new *game.py* file will look like the file below. 

```python
import pyxel
from sprites import Sprite

class Ball(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 6
        self.h = 6
        self.animation = ((1, 9), (9, 9), (17, 9))
        self.animation_index = pyxel.rndi(0,len(self.animation))

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
 
        self.sprite_list = []
        for _ in range(6):
            self.sprite_list.append(Sprite())
            self.sprite_list.append(Ball())           
        print(self.sprite_list)
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()
```

You added a different sprite, a ball, with its own position data and its own complex animation and movement logic by adding just a few lines of code to your game program. You did not need to ask the other programmer who maintains the *sprites.py* file to make any changes to their file. You can see how using classes can make reusing code easier and how classes support the concept of information hiding, resulting in program simplification.


# Conclusion

You build and object-oriented game program using Python classes and used concepts like information-hiding, encapsulation, and code re-use that help make programming easier. You got a taste of what it would be like to work on a larger project with other programmers and how the concepts you excercised in this tutorial can help.

You also learned about building games using the Pyxel framework and created a simple game animation. if you are interested, you will find it realtively easy to add more functionality to the game such as user input and collision detection. Please see the following link to see the source code for a full-featured game I created by extending the work already started in this turorial.



