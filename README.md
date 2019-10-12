# End2End GUI for Reinforcement Learning - [DEMO](end2endrl.web.app)

The common problem of maze solving is used in this framework. Where an agent has to learn to avoid the bad cells and reach the final state.

## How to use
  1. First, go to [DEMO](end2endrl.web.app). 
  2. Enjoy the already pretrained weights.
  3. Check the parameters, the 3D representations and the logs of the different environments.
  4. Try it out and create your own environment!
  5. Log in.
  6. Customize your environment.
  7. Train!
  8. Check the new environment after 5min or maybe 1 day!? It will depend on the difficulty of your problem.
  

## How to use (localhost master branch)
This is the easiest framework to play with RL: 
  1. First, go to localhost:3000. 
  2. Select the algorithm you want to use and then customize the available parameters. If you don't know which values should you use, leave the default values or select an already created environment and jump to step 7.
  3. Then you can customize the height and width of the grid. And also the walls, final and initial state positions.
  4. Save the environment! Now it should appear in the right-side list.
  5. If you are lucky, you'll find the server available, which means that you can train your faboulous environment. Click train and check the performance in the tensorboard provided.
  6. Once it is trained, you can evaluate the environment. From now on, you'll see a '3D' text next to your environment.
  7. Time to see the 3D representation! Just click the yellow 3D button an enjoy the learning process of your BB8.

## Algorithms
Currently we have only 4 algorithms available: Double DQN, Custom Genetic Algorithm, REINFORCE w/baseline and Actor-Critic. Take in consideration that every algorithm requires different parameters. Take the default values as reference and then make all the desired changes.
