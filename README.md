# AutoCastPy

Cast (Media) Websites through a web interface, with support for automation scripts.

* Intended for sites that do not have a Chromecast app.
* The web interface acts as a remote. // TODO
* Easily add or remove sites from the interface using a helper script. // TODO
* Write automation scripts to do certain actions on the site.


## Mapping file

The mapping file associates some segments of a URL with a userscript.
The name of the userscript has to be given without the .py ending.

Notice, that you can be as broad or strict with the URL segment as you want. 
However, the file is processed top down, so add strict entries before broad entries.

