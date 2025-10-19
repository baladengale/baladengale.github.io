const express = require('express');
const path = require('path');
const fs = require('fs');
const MarkdownIt = require('markdown-it');

const app = express();
const md = new MarkdownIt();

// Configuration
const config = {
    postsDir: path.join(__dirname, '..', 'posts'),
    contentDir: path.join(__dirname, '..', 'content'),
    outputDir: path.join(__dirname, '..', '..')
};

// Configure template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '..', 'templates'));

// Serve static files
app.use('/assets', express.static(path.join(config.outputDir, 'assets')));

// Parse frontmatter
function parseFrontMatter(content) {
    const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
    const match = content.match(frontmatterRegex);
    
    if (!match) {
        return {
            attributes: {},
            body: content
        };
    }

    const frontMatter = match[1];
    const body = match[2];
    const attributes = {};

    frontMatter.split('\n').forEach(line => {
        const [key, ...values] = line.split(':');
        if (key && values.length) {
            attributes[key.trim()] = values.join(':').trim();
        }
    });

    return { attributes, body };
}

// Get all posts
function getPosts() {
    const posts = fs.readdirSync(config.postsDir)
        .filter(file => file.endsWith('.md'))
        .map(file => {
            const content = fs.readFileSync(path.join(config.postsDir, file), 'utf8');
            const { attributes, body } = parseFrontMatter(content);
            const html = md.render(body);
            return {
                ...attributes,
                content: html,
                slug: file.replace('.md', '.html')
            };
        })
        .sort((a, b) => new Date(b.date) - new Date(a.date));
    
    return posts;
}

// Render a page with layout
app.get('/:page?.html', (req, res) => {
    const page = req.params.page || 'index';
    const contentPath = path.join(config.contentDir, `${page}.md`);
    
    try {
        const content = fs.readFileSync(contentPath, 'utf8');
        const { attributes, body } = parseFrontMatter(content);
        const html = md.render(body);
        
        res.render('layout', {
            content: html,
            css_path: './',
            ...attributes,
            posts: getPosts()
        });
    } catch (err) {
        res.status(404).send('Page not found');
    }
});

// Render blog posts
app.get('/posts/:slug.html', (req, res) => {
    const posts = getPosts();
    const currentPost = posts.find(post => post.slug === req.params.slug);
    
    if (!currentPost) {
        return res.status(404).send('Post not found');
    }
    
    // Get previous and next posts
    const currentIndex = posts.findIndex(post => post.slug === req.params.slug);
    const prevPost = posts[currentIndex + 1];
    const nextPost = posts[currentIndex - 1];
    
    res.render('layout', {
        ...currentPost,
        is_post: true,
        css_path: '../',
        prev_post: prevPost ? prevPost.slug : null,
        next_post: nextPost ? nextPost.slug : null,
        not_prev_post: !prevPost
    });
});

// Start server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});