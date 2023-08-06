# Ukedown package

Ukedown is a series of extensions to the standard
[Markdown library](https://github.com/Python-Markdown/markdown/tree/master/markdown), version 3 and higher
using the Extensions API, documented [here](https://python-markdown.github.io/extensions/api/)

It is intended to simplify songsheet (and songbook) generation for ukulele (although it work work well
for other stringed instruments too), allowing songsheets to be written as plain text,
which will be converted to HTML (via markdown) and thence to PDF.

All output styling will be done using CSS - examples of this are available
(with a toolset to use ukedown) from the [ukebook-md repository](https://github.com/lanky/ukebook-md)

Basic CSS to demonstrate is to be found in the 'css' subdir of the ukedown package itself.

This package uses [Semantic Versioning](https://semver.org/)

# What are these extensions anyway?

The following formatting is supported by ukedown:

## Titles and Artists
These are parsed from the first non-blank line in a `ukedown` file, and is expected to follow the format of

    Down Under - Men at Work

Where the separator is a normal ASCII hyphen (any Unicode m-dash and n-dash nonsense will be converted to ASCII).
These are rendered as `<h1>` elements in HTML
```html
<h1>Down Under - Men at Work</h1>
```

## Chord Names
Chord names appear inline with lyrics and are enclosed in parentheses.
These should be chord names only, with the exception that
characters such as '*' are supported - we use these in places to indicate 
single strums or stabs.

    At (Dm)first I was afraid, I was (Dm)petrified

These are rendered as `<span class="chord">` elements,as follows
```html
<span class="chord">Am</span>First I was afraid I was <span class="chord">Dm</span>petrified,<br/>
```

## section headers
Basically song section titles like "verse 1" and "chorus".

These are enclosed in square brackets, like this:
    
    [intro]

They are rendered as `<span class="section_header">` elements.
Because they are inline, they can have chords and other items on the same line if required.
```html
<span class="section_header">intro<span>
```


## Performance notes
Things like *slowly* or *single strums* or *fade out*

These are enclosed in curly braces

    {slowly}

although they appear in rendered documents as 
```html
<span class="notes">slowly</span>
```

## Backing vocals
Currently these are delimited in the same fashion as chords, and are distinguished by **not** matching a known chord pattern.
This is likely to change (most probably to `<>` or `::`) to simplify the rendering and to allow nesting of elements, which currently doesn't work properly (e.g. chords inside backing vox)

    (you're gonna wish you, never had met me)

## boxed sections
when certain sections of a song repeat, it's quite common to put them into 'boxes' - this is done using `|` (pipe) characters.
Any line starting with (and optionally ending with) a '|' character will be rendered as a 'boxout'

Boxes can also contain section headings, as shown

    | [chorus]
    | But I'm a (G)creep
    | I'm a (B7)weirdo
    | What the hell am I doing (C)here
    | I don't be(Cm)long here

which will render as 
```html
<div class="box">
  <p><span class="section_header">chorus</span><br/>
  But I'm a <span class="chord">G</span>creep<br/>
  I'm a <span class="chord">B7</span>weirdo<br/>
  What the hell am I doing <span class="chord">C</span>here<br/>
  I don't be<span class="chord">Cm</span>long here</p>
  </div>
```

### current limitations
repeated boxes (i.e. 2 boxed sections in a row, which occasionally happens) *must* have a blank line between them, or they get merged into one box.

## Hang on, where are all my brackets/parentheses/braces etc?
ukedown itself only uses these to identify chords/backing vocals etc - it is up to you to decide if they should be in the final output. In fact if you want to render them completely differently you can, as they can be styled using CSS.

### CSS providing brackets
The following renders chord names with the delimiting () parentheses, without the `:before` and `:after` parts the would just be chord names.

```css
.chord {
    font-weight: bold;
}

.chord:before {
    content: "(";
}
.chord:after {
    content: ")";
}
```

# Style
Ukedown only produces HTML elements with named classes, it does no styling itself - this should be done using CSS. A sample CSS example follows:

```css
@charset 'utf-8';

.indexlink {
    text-decoration: none;
    font-size: 0.9em;
    color: inherit;
}

.chord {
    font-weight: bold;
}

.chord:before {
    content: "(";
}
.chord:after {
    content: ")";
}

.section_header {
    font-weight: bold;
    font-size: 1em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    padding-bottom: 0.5em;
}

.section_header:before {
    content: '[';
}

.section_header:after {
    content: ']';
}

.vox {
    font-weight: normal;
    font-style: italic;
}

.vox:before {
    content: "(";
}

.vox:after {
    content: ")";
}

.notes {
    font-style: normal;
    font-weight: bold;
}
.notes:before {
    content: "[";
}
.notes:after {
    content: "]";
}

p {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}

/* Box call-outs (repeated chorus etc) */
.box {
    padding: 5px;
    padding-top: 0;
    padding-bottom:0;
    border-left: 2px solid black;
    width: auto;
    max-width: 98%;
    margin: 2px;
    margin-bottom: 0.5em;
}

.box > p {
    margin-top: 0;
    margin-bottom: 0;
    margin-left: 5px;
}

.box > p:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
}

.box > h2, .section_header {
    margin-top: 0;
    padding-top: 0;
    padding-bottom: 0;
    margin-bottom: 0;
}

/* End box definitions*/
```
