# WSF local website

Open `index.html` in a browser. It works directly from the filesystem as well as from a static web server.

## Editing content

Edit the five Markdown documents in `docs/`, then regenerate the page:

```sh
python3 build-pages.py
```

Run the command from this directory, or supply the full path to the script. No additional packages are required. The builder supports the headings, paragraphs, bullet lists, emphasis, and links used in these documents. Internal document links open the corresponding website section.

`page-template.html` contains the shared design, landing page, navigation, and footer. `index.html` is generated; content changes belong in the Markdown sources. Each document page includes a download link to its Markdown source.

The census and discussion-paper descriptions are drafts. They describe proposed work rather than completed research or a populated database.
