# majors_site

Stack: Django + Redis + Celery + PostgreSQL + docker.  

This project is responsible for the entire website and user interactions, serving as a bridge between users and data stored on other servers. This approach ensures system independence and resilience.  

Implemented functionality includes:  

    Subscription system
    Customizable blog
    Payment processing
    Utilization of best practices for protection against various vulnerabilities

To set up this project, you need to create a secrets.py file in the myproject directory and specify the details for PostgreSQL and Redis for Celery on this server, as well as cache settings and two caches on other servers. Additionally, you should provide email information for sending emails.

Also, make sure to install PostgreSQL and Redis:  
docker run --name my-postgres-container -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres  
docker run --name my-redis-container -d -p 6379:6379 redis  
