
# openKB - Django Version

![logo](https://files.markmoffat.com/openkb/logo.png)

openKB is a Markdown Knowledge base application (FAQ) built with Django. It is designed to be easy to use and install, with a focus on search functionality rather than nested categories. Simply search for what you want and select from the results.

### Installation

1. Clone the Repository: `git clone https://github.com/yourusername/openKB-Django.git && cd openKB-Django`
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Apply migrations:
   ```bash
   poetry run python manage.py migrate
   ```
4. Start the application:
   ```bash
   poetry run python manage.py runserver
   ```
5. Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser

### Features

- **Search**: openKB is a search-based Knowledge base (FAQ) using Django ORM to query and return relevant articles.
- **Responsive Design**: Built using Bootstrap, allowing the application to be responsive and work on all devices.
- **Markdown Support**: Uses Markdown for article content, allowing easy and flexible content formatting.
- **User Authentication**: Includes user authentication with the ability to set up the first admin user on the first login attempt.
- **File Management**: Allows file uploads with dynamic directory choices and file management capabilities.
- **Google Analytics Integration**: Ability to add Google Analytics tracking code for monitoring site usage.
- **Configurable Settings**: Customize website, article, display, and style settings via the admin interface.

### Screenshots

**Homepage**

![Homepage](https://files.markmoffat.com/openkb/homepage.png)

**Admin Editor**

![Editor](https://files.markmoffat.com/openkb/editor.png)

**Article View**

![Article view](https://files.markmoffat.com/openkb/articleview.png)

**Admin Article Management**

![Article filtering](https://files.markmoffat.com/openkb/articlefiltering.png)

**Managing Files**

![Files](https://files.markmoffat.com/openkb/files.png)

### Admin

Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

The first-time setup will prompt the creation of an admin user. Subsequent logins will redirect to the standard login page.

### Configuration

Configuration can be done via the `/settings` page in the admin interface or the settings page in the user interface.

#### Website Settings

- `website_title`: The title of your website.
- `website_description`: A short description that appears in search engine results.
- `show_website_logo`: Toggle to show or hide the website logo.
- `base_url`: The root URL where your site is hosted. E.g., http://example.com/
- `allow_api_access`: Allow external systems to access site data via API.
- `api_token`: The security token others will use to access your API.
- `password_protect`: Require users to log in before accessing the site.
- `index_article_body`: Include the text of articles in the search index.
- `select_theme`: The visual theme for the site.
- `select_language`: The language the site interface will appear in.
- `show_logon_link`: Display a link for users to log on if needed.
- `date_format`: Format in which dates are displayed on the site.
- `article_suggestions_allowed`: Allow users to submit articles for potential inclusion.
- `google_analytics_code`: Google Analytics code to track site usage.

#### Article Settings

- `allow_voting`: Allow users to vote on articles.
- `show_article_meta`: Show article metadata, including published date and author.
- `show_author_email`: Display the author's email in the metadata.
- `article_links_open_new_page`: Open links in articles in a new page/tab.
- `add_header_anchors`: Add HTML anchors to all heading tags for linking within articles.
- `enable_editor_spellchecker`: Enable spellchecker in the editor.
- `allow_article_versioning`: Track article versions with each save.
- `allow_mermaid`: Enable Mermaid charts within articles.
- `allow_mathjax`: Enable MathJax within articles.

#### Display Settings

- `number_of_top_articles`: Number of results shown on the homepage.
- `show_published_date`: Display the published date next to results.
- `show_view_count`: Display the view count next to results.
- `update_view_count_when_logged_in`: Update view count when users are logged in.
- `show_featured_articles`: Display featured articles in a sidebar.
- `featured_article_count`: Number of featured articles shown.

#### Style Settings

- `header_background_color`, `footer_background_color`: Color settings for header and footer backgrounds.
- `header_text_color`, `footer_text_color`: Color settings for header and footer texts.
- `button_background_color`, `button_text_color`: Color settings for button backgrounds and texts.
- `link_color`: Color setting for links.
- `page_text_color`: Color setting for page text.
- `page_font`: Font setting for the page.

### Additional Features

- **Dynamic File Uploads**: Choose upload directories dynamically.
- **Initial Setup**: First-time setup prompts for admin account creation.
- **Integrated Search**: Real-time search filtering of articles on the homepage and article list pages.
- **Export Functionality**: Export all published articles as Markdown files in a zipped archive.

### Contributing

Feel free to contribute by submitting issues, feature requests, or pull requests.

### Running in Production

Using [Gunicorn](https://gunicorn.org/) or [Daphne](https://github.com/django/daphne) with a server like Nginx is recommended for running Django applications in production.
