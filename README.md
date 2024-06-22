# Lichess Bot

The backend of a [lichess bot](https://lichess.org/@/Bot5551), that's running a leela chess engine, trained to play like me based on [my lichess games](https://lichess.org/@/Red5551).
The training was done using [maia-individual](https://github.com/donaldflynn/maia-individual), and the hosting is done using lichess-bot, which this repositry is forked from.

## Performance

- The bot seems to generally perform quite well, and plays moves similar to ones that I would play. During the training the logs said that it would play the same move as me somewhere between 60-70% of the time - though it's quite hard to judge if this is good from just the numbers.
- It does have a tendancy to make random catastrophic blunders (so perhaps it is too accurate!) The performance is also very dependant on the hardware. There's docker containers for running on both a raspberry pi, and on a system with access to an nvidia graphics card.
- The bot plays very similar chess openings to me - though at some point I might include an opening book, as it currently takes its time on the first few moves. I should also introduce some randomisation, as the openings are purely deterministic so it can get a bit repetetive. In theory it should be looking up my games on lichess at the moment, but in practise this seems to fail quite often, so it'd be better to access to some offline book. 


## Links
- [Play the bot (assuming there's an instance running somewhere)](https://lichess.org?user=Bot5551#friend)
- [Original lichess-bot repo](https://github.com/lichess-bot-devs/lichess-bot)
- [Maia project](https://maiachess.com/)

## Running the code
### For raspberry pi:
1. Build docker container with `scripts/build_docker_pi.bat`
2. If you've not done multi-arch builds before on your machine, you may need to set it up with: ```docker run --rm --privileged multiarch/qemu-user-static --reset -p yes```
