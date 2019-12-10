![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fjuanjo3ns%2Fend2endRL)
# End2End GUI for Reinforcement Learning - [DEMO](https://end2endrl.web.app)

Teach an agent to solve custom mazes using Reinforcement Learning!

### Warning! The code actually being used can be found at the redesign branch.

## How it is everything working
As you will notice this frankestein project is a clear example of a low cost project.
We are using a gpu in a server of our university to carry out all the experiments. It is a basic GTX 1060 with 6gb of ram. All this code is done in python and the deep learning framework that we've been using is Pytorch!
The frontend is deployed in firebase and for developing it we have used React. Firebase has been very helpful as well for authentication of users and also as a database.
Finally, we also have a tensorflow cpu container running in aws for serving the logs of all the experiments. Yes, they are automatically upload it from our server to aws every time an experiment is finished.

## How to use (Deployed version - redesign branch)
  1. First, go to [DEMO](end2endrl.web.app). 
  2. Enjoy the already pretrained environments.
  3. Check the parameters, the 3D representations and the logs of the different environments.
  4. Try it out and create your own environment!
  5. Log in.
  6. Customize your environment.
  7. Train!
  8. Check the new environment after 5min or maybe 1 day!? It will depend on the difficulty of your problem.
  

## How to use (localhost master branch)
This is the easiest framework to play with RL: 
  ### Requirements:
    - Docker
    - Docker-compose
    - Nvidia-docker
  ### Steps
  1. Clone repo.
  2. In the docker compose uncomment the line command: flask run, and comment the line below.
  3. make run
  4. Go to localhost:3000. 
  3. Select the algorithm you want to use and then customize the available parameters. If you don't know which values should you use, leave the default values or select an already created environment and jump to step 7.
  4. Then you can customize the height and width of the grid. And also the walls, final and initial state positions.
  5. Save the environment! Now it should appear in the right-side list.
  6. If you are lucky, you'll find the server available, which means that you can train your faboulous environment. Click train and check the performance in the tensorboard provided.
  7. Once it is trained, you can evaluate the environment. From now on, you'll see a '3D' text next to your environment.
  8. Time to see the 3D representation! Just click the yellow 3D button an enjoy the learning process of your BB8.

## Algorithms
Currently we have only 4 algorithms available: Double DQN, Custom Genetic Algorithm, REINFORCE w/baseline and Actor-Critic. Take in consideration that every algorithm requires different parameters. Take the default values as reference and then make all the desired changes.
