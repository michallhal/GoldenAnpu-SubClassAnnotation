# GoldenAnpu-SubClassAnnotation
Provides annotation support for the GoldenAnpu sweet pepper dataset to convert it to the University of Bonn BUP variants.

This GUI was created in PyQt6.

# Create the virtual environment

Using python3 create your virtual environment

You may need to follow [this](https://askubuntu.com/questions/1434956/install-qt6-on-22-04) guide to install PyQt6 on your machine.

```python3 -m venv venv-GUI```


```>>> . venv-GUI/bin/activate```
```>>> pip3 install -r requirements.txt```


# Download the GoldenAnpu Sweet Pepper Dataset

Go to [here](https://github.com/dataset-ninja/sweet-pepper) and then click on the ```DOWNLOAD.md``` document and follow the prompts.

You'll find the meta file for their dataset [here](files/meta.json) that you need to put in the root directory you downloaded.

# Run the annotation tool

```>>> python main.py --root <root location of the dataset> --imageloc <direct location to the images> --annoloc <direct location to the image jsons> --output <where you'd like to save the corrosponding smap and imap images>```

# How to use the annotation tool

![Screenshot of the Application](images/GUI.png)

This is a basic subclass annotation tool for existing instance-based semantic segmentation datasets that have json files in the ```supervisely``` library type fashion.

The main image is displayed on the left panel with the object outlined based on the colours in the [meta](files/meta.json) file, you can change these as you wish.

The middle panel is the zoomed in and cropped object. On the right is the subclass buttons.

```MRed == mixed red```

```MYellow == mixed yellow```

For each annotation per image the button for the currently annotated sub-class will be depressed. If this is incorrect, you need to press that button then select the correct sub-class (you can do this in any order).
Once you have either changed the sub-class or are happy with them you hit the next button and the next annotation will be displayed.

If you made a mistake, you can hit the back button and you will go back to the previous annotation. **WARNING** if you go back far enough that you enter the previous image you will start that image from the beginning!

Finally, there is no save function, if you want to start again from a particular image you can use the ```image index``` drop down menu.
Look in the ```--output``` directory, work out which image you are up to, then select that image from the drop down menu.
