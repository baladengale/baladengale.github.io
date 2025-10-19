const path = require('path');
const fs = require('fs');
const express = require('express');
const MarkdownIt = require('markdown-it');

// Configuration
const config = {
    postsDir: path.join(__dirname, '..', 'posts'),
    contentDir: path.join(__dirname, '..', 'content'),
    outputDir: path.join(__dirname, '..', '..')
};

// Initialize markdown parser
const md = new MarkdownIt();

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
    return fs.readdirSync(config.postsDir)
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
}

// Read template
const template = fs.readFileSync(path.join(__dirname, '..', 'templates', 'layout.html'), 'utf8');

// Build a page
function buildPage(templateContent, data) {
    let html = templateContent;
    
    // Replace variables
    Object.entries(data).forEach(([key, value]) => {
        const placeholder = new RegExp(`\\$${key}\\$`, 'g');
        html = html.replace(placeholder, value || '');
    });
    
    // Handle conditionals
    html = html.replace(/\$if\((.*?)\)(.*?)\$endif\$/gs, (match, condition, content) => {
        return data[condition] ? content : '';
    });
    
    return html;
}

// Build all pages
function buildSite() {
    const posts = getPosts();
    
    // Build regular pages
    ['index', 'blog', 'about'].forEach(page => {
        const contentPath = path.join(config.contentDir, `${page}.md`);
        if (fs.existsSync(contentPath)) {
            const content = fs.readFileSync(contentPath, 'utf8');
            const { attributes, body } = parseFrontMatter(content);
            const html = md.render(body);
            
            const pageData = {
                content: html,
                css_path: './',
                ...attributes,
                posts: JSON.stringify(posts)
            };
            
            const renderedPage = buildPage(template, pageData);
            fs.writeFileSync(path.join(config.outputDir, `${page}.html`), renderedPage);
        }
    });
    
    // Build blog posts
    posts.forEach((post, index) => {
        const prevPost = posts[index + 1];
        const nextPost = posts[index - 1];
        
        const postData = {
            ...post,
            is_post: true,
            css_path: '../',
            prev_post: prevPost ? prevPost.slug : '',
            next_post: nextPost ? nextPost.slug : '',
            not_prev_post: !prevPost
        };
        
        const renderedPost = buildPage(template, postData);
        fs.writeFileSync(path.join(config.outputDir, 'posts', post.slug), renderedPost);
    });
}

// Execute build
buildSite();