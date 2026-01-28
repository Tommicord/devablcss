from devabl import css, conf, minify, dist, watch

def main() -> None:
     csss = css()
     csss.pipelist(
          csss.pipes # start the pipeline
          .pipe(conf, {
               "root": "./src",
               "out": "./css.css",
               "include": ["./src/**/*.py"]
          }) # configure paths
          .pipe(minify) # minify the CSS
          .pipe(dist, open=False) # open=False to prevent automatic opening
          .pipe(watch) # watch for changes
     )

main()