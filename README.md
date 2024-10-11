# move-files-to-docs-folder

Move files to docs folder github action and update mkdocs.yml during build. 
Intended to be used before a build step that runs the following command:

```
techdocs-cli generate --no-docker --verbose
```