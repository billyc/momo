# MoMo Website files

This is a "static" website, built using Jekyll and hosted on GitHub Pages

### Installation

- Install Ruby 3.1+
- Run `bundle install`

### Run a local development server

- Edit `config.yml` to match your site requirements
- Run `bundle exec jekyll serve` to run a local copy of the site.

You can make changes and it will auto-rebuild; then click reload on your browser to see your changes.

### To build it yourself:

- Run `bundle exec jekyll build`

That will build the site in the `_site` directory.

Note that we use GitHub Actions to auto-build and publish the site when new commits are pushed to the `main` branch on GitHub.

That build process is defined in `.github/workflows/build-jekyll.yml`.
