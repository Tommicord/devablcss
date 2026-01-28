# Devabl CSS

A python framework for creating dynamic and configurable CSS stylesheets using a templating approach, using themes, conditions, and reusable components.

## Example

```python
from devabl import pipes, css, minify, conf, render

a = <? # Open a CSS template
     @theme DarkMode
          :root {
               --background-color: black;
               --text-color: white;
          }
     @end theme 

     @theme LightMode
          :root {
               --background-color: white;
               --text-color: black;
          }
     @end theme 
     
     @dynamic
          @if($condition) 
               @then DarkMode
          @else
               @then LightMode 
          @endif
     @end dynamic
?>

styles = css()
styles.pipelist(
     csss = css()
     csss.pipelist(
          csss.pipes # start the pipeline
          .pipe(render, a) # render the template
          .pipe(conf, {
               "root": "./src",
               "out": "./css.css",
               "include": ["./src/**/*.py"]
          }) # configure paths
          .pipe(minify) # minify the CSS
          .pipe(dist, open=False) # open=False to prevent automatic opening
          .pipe(watch) # watch for changes
     )
)
```

And you execute in terminal:

```bash
devabl your_file.py
```

This will generate a minified CSS file at `./styles/app.css` based on the condition provided.

Very similar to PHP templating, but for CSS generation. pipe syntax inspired by Gulp.js and other task runners.

## Why use pipes?
Pipes allow for modular and reusable processing steps when generating CSS. Each pipe can perform a specific task, such as minification, rendering templates, or configuration management. This modularity makes it easy to customize and extend the CSS generation process according to your project's needs.

## Devabl or Tailwind CSS?
Devabl CSS focuses on dynamic CSS generation through Python code, allowing for complex logic and conditions. Tailwind CSS is a utility-first CSS framework that provides pre-defined classes for rapid UI development. Choose Devabl for dynamic styles and Tailwind for quick prototyping with utility classes.

## Why Devabl is in Python?
- Devabl is built in Python to leverage its simplicity, readability, and extensive libraries. Python's
- Devabl ecosystem allows for easy integration with other tools and frameworks, making it a versatile choice for developers looking to create dynamic CSS stylesheets.
- Python has no native CSS generation tools, so Devabl fills that gap.
- Python has no much competition in this space, making Devabl a unique offering.
- JavaScript already has many CSS-in-JS solutions, so Devabl aims to provide a similar experience for Python developers.
- Python has no new syntax for CSS generation, making Devabl a fresh approach.

Work in progress. More features coming soon!