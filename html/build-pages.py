#!/usr/bin/env python3
"""Build the static WSF page from page-template.html and docs/*.md (no dependencies)."""
from pathlib import Path
import html
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
PAGES = [
    ('why', 'why-i-started-wsf.md', 'Todd Ringler'),
    ('premise', 'working-premise.md', 'The idea I am testing'),
    ('approach', 'initial-approach.md', 'From initial work to an informed decision'),
    ('census', 'census-project-description.md', 'Initial project'),
    ('marine', 'discussion-paper-description.md', 'Initial project'),
    ('disclosures', 'disclosures.md', 'Transparency'),
]
ROUTES = {filename: page for page, filename, _ in PAGES}


def inline(text):
    value = html.escape(text)
    def link(match):
        label, url = match.groups()
        if url in ROUTES:
            target = ROUTES[url]
            return f'<a href="#{target}" data-wsf-page="{target}">{label}</a>'
        if not url.startswith(('https://', 'http://', '#')):
            raise ValueError(f'Unsupported link: {url}')
        return f'<a href="{html.escape(html.unescape(url), quote=True)}">{label}</a>'
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', value)


def render(markdown, page):
    blocks = re.split(r'\n\s*\n', markdown.strip())
    output, headings = [], []
    for block in blocks:
        lines = block.splitlines()
        heading = re.fullmatch(r'(#{1,3}) (.+)', block)
        if heading:
            level, text = len(heading[1]), heading[2]
            slug = page + '-' + re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            output.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>')
            if level == 2:
                headings.append((slug, text))
        elif all(line.startswith('- ') for line in lines):
            output.append('<ul>' + ''.join('<li>' + inline(line[2:]) + '</li>' for line in lines) + '</ul>')
        else:
            if any(line.startswith(('# ', '## ', '### ', '- ')) for line in lines):
                raise ValueError('Separate headings and lists with blank lines')
            output.append('<p>' + inline(' '.join(lines)) + '</p>')
    if page == 'approach':
        toc = '<nav class="contents" aria-label="On this page"><span>On this page</span><ul>'
        toc += ''.join(f'<li><a href="#{slug}">{inline(text)}</a></li>' for slug, text in headings)
        toc += '</ul></nav>'
        output.insert(1, toc)
    return '\n'.join(output)


def build():
    panels = []
    for page, filename, eyebrow in PAGES:
        source = ROOT / 'docs' / filename
        markdown = source.read_text()
        document = render(markdown, page)
        title = markdown.splitlines()[0].removeprefix('# ')
        subject = quote('WSF feedback: ' + title, safe='')
        mailto = 'mailto:comments@wildsteelheadfutures.org?subject=' + subject
        comment_link = f'<a class="comment-link" href="{mailto}">Comment on this page <span aria-hidden="true">↗</span></a>'
        feedback = f'<aside class="feedback" aria-label="Share feedback"><h2>What do you think?</h2><p>Questions, corrections, and different perspectives are welcome.</p><p>{comment_link}</p><p class="feedback-address">Opens your email app. You can also write to <a href="{mailto}">comments@wildsteelheadfutures.org</a>.</p></aside>'
        panels.append(f'<section id="wsf-{page}" role="tabpanel" aria-labelledby="wsf-tab-{page}" hidden><article class="document"><div class="document-meta"><div class="eyebrow">{eyebrow}</div>{comment_link}</div>\n{document}\n{feedback}\n<p class="document-download"><a href="docs/{filename}" download>Download Markdown</a></p></article></section>')
    template = (ROOT / 'page-template.html').read_text()
    assert template.count('{{DOCUMENT_PANELS}}') == 1
    output = template.replace('{{DOCUMENT_PANELS}}', '\n'.join(panels))
    (ROOT / 'index.html').write_text(output)
    print(f'Built {len(PAGES)} document pages in {ROOT / "index.html"}')


if __name__ == '__main__':
    build()
