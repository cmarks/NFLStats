# NFLData Notes

### Azure Database for Postgres

- General Information
    - Server name: [nfldatapg.postgres.database.azure.com](http://nfldatapg.postgres.database.azure.com/)
    - Database name: postgres (Default)
    - Username: user
    - Password: secret123!
    - Entity-Relationship-Diagram (ERD): [https://lucid.app/lucidchart/e9acfd3f-8f78-4a69-8496-eed292e94e6e/edit?invitationId=inv_109497e2-e24b-4389-9108-e460933b61d8](https://lucid.app/lucidchart/e9acfd3f-8f78-4a69-8496-eed292e94e6e/edit?invitationId=inv_109497e2-e24b-4389-9108-e460933b61d8)
    - Network Rules:
        - Current network settings allow access from any server and IP address
        - To edit these settings, go to Networking tab under Settings and edit firewall rules
- Migrating entire local Postgres database to Azure Database for Postgres: [https://docs.microsoft.com/en-us/azure/postgresql/howto-migrate-using-dump-and-restore](https://docs.microsoft.com/en-us/azure/postgresql/howto-migrate-using-dump-and-restore)
- Helpful IDE for interacting with Azure Database for Postgres
    - [https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15](https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15)
    - Must install PostgreSQL extension to work with Azure Database for Postgres: [https://docs.microsoft.com/en-us/sql/azure-data-studio/quickstart-postgres?view=sql-server-ver15](https://docs.microsoft.com/en-us/sql/azure-data-studio/quickstart-postgres?view=sql-server-ver15)

### Deepnote

- General Information
    - Link: [https://deepnote.com](https://deepnote.com/)
    - Deepnote is a data science notebook hosted in the cloud
    - Python scripts can be run with the output displayed
- Calculating estimated cash and salary cap losses by games missed due to injury: [https://deepnote.com/project/NFLData-QzND-rWHRJObuYLF6icfoA/%2FCostsPerGameMissed.ipynb](https://deepnote.com/project/NFLData-QzND-rWHRJObuYLF6icfoA/%2FCostsPerGameMissed.ipynb)

### Power BI Notebook

- General Information
    - Tool for creating reports from data sources