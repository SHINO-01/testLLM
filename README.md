<body>
    <header>
        <h1>LLM Django CLI Project</h1>
    </header>
    <section id="introduction">
        <h2>Introduction</h2>
        <p>
            This project demonstrates the integration of Django CLI commands with Scrapy and the Gemini API to
            manage, rewrite, and generate data dynamically. It features a modular architecture that handles hotel
            data scraping, rewriting descriptions, generating summaries, and creating fake reviews and ratings.
        </p>
    </section>
    <section id="table-of-contents">
        <h2>Table of Contents</h2>
        <ul>
            <li><a href="#folder-structure">Folder Structure</a></li>
            <li><a href="#dependencies">Dependencies</a></li>
            <li><a href="#system-architecture">System Architecture</a></li>
            <li><a href="#setup">How to Download and Setup the Project</a></li>
            <li><a href="#run-project">How to Run the Project</a></li>
            <li><a href="#sample-outputs">Sample Outputs</a></li>
            <li><a href="#test-project">How to Test</a></li>
            <li><a href="#known-issues">Known Issues</a></li>
        </ul>
    </section>
    <section id="folder-structure">
        <h2>Folder Structure</h2>
        <pre>
        ├── llm_django/
        │   ├── settings.py          # Django project settings
        │   ├── urls.py              # URL configuration
        │   ├── wsgi.py              # WSGI application
        │   └── __init__.py
        ├── llm_cli_cmds/
        │   ├── management/
        │   │   └── commands/
        │   │       ├── run_rewrite.py    # CLI for rewriting data
        │   │       ├── run_scrapy.py     # CLI for triggering Scrapy
        │   │       └── __init__.py
        │   ├── models.py            # Models for database tables
        │   ├── tests/               # Unit tests for the application
        │   │   └── test_cmds.py
        │   └── __init__.py
        ├── scrapy_project/          # Scrapy project files
        ├── manage.py                # Django entry point
        ├── requirements.txt         # Dependencies
        └── README.html              # Project documentation
        </pre>
    </section>
    <section id="dependencies">
        <h2>Dependencies</h2>
        <ul>
            <li>Python 3.11</li>
            <li>Django</li>
            <li>Scrapy</li>
            <li>PostgreSQL</li>
            <li>psycopg2</li>
            <li>requests</li>
            <li>coverage</li>
        </ul>
    </section>
    <section id="system-architecture">
        <h2>System Architecture</h2>
        <p>
            The project follows a modular design with two primary components:
        </p>
        <ul>
            <li><strong>Django:</strong> Handles CLI commands and database management.</li>
            <li><strong>Scrapy:</strong> Scrapes hotel data and stores it in the PostgreSQL database.</li>
        </ul>
        <p>
            Data flows between these components via a shared database, allowing seamless integration.
        </p>
    </section>
    <section id="setup">
        <h2>How to Download and Setup the Project</h2>
        <ol>
            <li>Clone the repository:</li>
            <pre><code>git clone https://github.com/SHINO-01/testLLM.git</code></pre>
            <li>Navigate to the project directory:</li>
            <pre><code>cd testLLM</code></pre>
            <li>Install dependencies:</li>
            <pre><code>pip install -r requirements.txt</code></pre>
            <li>Set up the environment variables in a <code>.env</code> file:</li>
            <pre>
GEMINI_API_KEY=your-gemini-api-key
            </pre>
            <li>Run the Docker-compose File</li>
            <pre><code>docker-compose up --build</code></pre>
            <li>Run migrations:</li>
            <pre><code>docker exec -it Django_LLM python manage.py makemigrations</pre></code>
            <pre><code>docker exec -it Django_LLM python manage.py migrate</pre></code>
        </ol>
    </section>
    <section id="run-project">
        <h2>How to Run the Project</h2>
        <ol>
            <li>Access the pgAdmin Page:</li>
            <pre>localhost:5050</pre>
            <li>Use the following credentials:</li>
            <ul>
                <li>Admin ID: <code>admin@admin.com</code></li>
                <li>Admin Pass: <code>admin123</code></li>
                <li>Register Server:-->HostName: llm_db_cont</li>
                <li>POSTGRES_USER: shino, POSTGRES_PASSWORD: shinopass123, POSTGRES_DB: llm_test_DB</li>
            </ul>
            <ul>
              <li>Commands for Running Scrapper: <pre><code>docker exec -it LLM_Django python manage.py run_scrapy</code></pre></li>
              <li>Commands for Running Rewrite using LLM: <pre><code>docker exec -it LLM_Django python manage.py run_rewrite</code></pre></li>
            </ul>
        </ol>
    </section>
    <section id="sample-outputs">
        <h2>Sample Outputs</h2>
        <h3>Rewritten Data:</h3>
        <pre>
        Title: "Modern Hotel in City Center"
        Description: "Experience luxury at its finest with our state-of-the-art amenities..."
        </pre>
        <h3>Generated Summary:</h3>
        <pre>
        Summary: "A luxurious hotel located in the heart of the city, offering top-notch facilities."
        </pre>
        <h3>Fake Review:</h3>
        <pre>
        Review: "The room was spacious and clean. Excellent customer service!"
        Rating: 4.5
        </pre>
    </section>
    <section id="test-project">
        <h2>How to Test</h2>
        <ol>
            <li>Run the test suite:</li>
            <pre><code>docker exec -it LLM_Django coverage run manage.py test llm_cli_cmds/tests/</code></pre>
            <li>Generate a coverage report:</li>
            <pre><code>ddocker exec -it LLM_Django coverage report</code></pre>
        </ol>
    </section>
    <section id="known-issues">
        <h2>Known Issues</h2>
        <ul>
            <li>Test database conflicts if not properly cleaned up.</li>
            <li>Gemini API rate limits may affect batch processing.</li>
        </ul>
    </section>
</body>
