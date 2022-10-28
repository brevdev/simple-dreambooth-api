Huge thanks to [Shivam Shrirao](https://github.com/ShivamShrirao) for providing us his implementation of DreamBooth. 

To get started, hit this [link](https://console.brev.dev/environment/new?setupRepo=https://github.com/brevdev/dreambooth&repo=https://github.com/brevdev/dreambooth&setupPath=.brev/setup.sh&instance=g5.2xlarge)to create a Brev environment. We've pre-configured the defaults you'll need to run DreamBooth.

Install Brev:
```
brew install brevdev/homebrew-brev/brev
```
Then open your new DreamBooth environment in VSCode:
```
brev open dreambooth --wait
```

Once you're in, upload about 20 or so photos of someone you want to generate SD samples of. 
Inside launch.sh, change INSTANCE_DIR to point to the folder you stored the training samples of.

Then you can change the prompts you use on lines 13 and 22 of launch.sh

To run do:
```
sh launch.sh
```
It'll prompt you to add your huggingface token and then the model should download and fine-tune on your input images 🎉🎉. (It should take around 7 minutes to train and generate samples!)


To explore more options have a look at [Shivam's example](https://github.com/ShivamShrirao/diffusers/tree/main/examples/dreambooth)