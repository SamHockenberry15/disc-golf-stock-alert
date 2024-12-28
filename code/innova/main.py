from file_retriever import FileRetriever
from constants import INNOVA

if __name__ == '__main__':
    # Download Latest File to Local
    FileRetriever(INNOVA).retrieve_data()


    # Parse File

    # Maybe store data in a SQLite DB?

    # Run query to complete an outer join to see what has changed day-by-day

    # Maybe app can do a 1 day, 7 day, and 30 day comparison
