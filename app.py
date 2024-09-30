# from crypt import methods
# from dbm import error

import logging
logging.basicConfig(level=logging.DEBUG)


from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import random
import wikipediaapi

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

with open('books.pkl', 'rb') as f:
    books_df = pickle.load(f)
    bookslist = books_df.to_dict(orient='records')

# print(f"Type of books: {type(books)}")
# print("First few entries in books:")
# print(books[:5])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/top50')
def top50():
    # popbooks = popular_df.to_dict(orient='records')

    unique_books = popular_df.drop_duplicates(subset=['Book-Title'], keep='first')

    # Merge to get the ISBN from the books_df
    unique_books = unique_books.merge(books_df[['ISBN', 'Book-Title']], on='Book-Title', how='left')

    # Use a set to track seen book titles
    seen_titles = set()
    books = []
    
    for _, book in unique_books.iterrows():
        title = book['Book-Title']
        author = book['Book-Author']
        isbn = book['ISBN']

        # Check if the book title has already been seen and if both description and author are available
        if title not in seen_titles and isbn:  # Add any additional conditions needed
            seen_titles.add(title)
            books.append(book)


    return render_template('top50.html',
                           books = books,
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input').strip().lower()

    if user_input == "":
        return render_template('recommend.html', data=None, error="Invalid Input")

    keywords = user_input.split()
    matching_indices = []
    for i, title in enumerate(pt.index):
        title_lower = title.lower()
        if all(keyword in title_lower for keyword in keywords):
            matching_indices.append(i)

    if len(matching_indices) == 0:
        return render_template('recommend.html', data=None, error="No such book exists in our database")
    else:
        index = matching_indices[0]  # Access the first matching index safely
        print(f"Data found at index: {index}")

    # Get similar books based on the similarity scores for the matched book
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:4]

    data = []
    for i in similar_items:
        item = []
        # Extract book details, including ISBN
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['ISBN'].values))  # Get the ISBN code

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)




@app.route('/searchbygenre')
def searchbygenre():
    return render_template('searchbygenre.html')

# @app.route('/searchbygenre/fantasy', methods=['post'])
# def fantasy():
#     ideal_book = "Harry Potter and the Sorcerer's Stone (Book 1)"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)


# @app.route('/searchbygenre/comedy', methods=['post'])
# def comedy():
#     ideal_book = "The Nanny Diaries: A Novel"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)

# @app.route('/searchbygenre/horror', methods=['post'])
# def horror():
#     ideal_book = "Midnight"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)








def get_genre_books(ideal_book,num):
    matching_indices = np.where(pt.index == ideal_book)[0]
    if not matching_indices.size:
        return render_template('searchbygenre.html', data=None, error="No such book exists in our database")

    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:num]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        temp_df = temp_df.drop_duplicates('Book-Title')
        item.extend(list(temp_df['Book-Title'].values))
        item.extend(list(temp_df['Book-Author'].values))
        item.extend(list(temp_df['Image-URL-M'].values))
        item.extend(list(temp_df['ISBN'].values))  # Include ISBN for redirection
        data.append(item)

    return render_template('searchbygenre.html', data=data)


@app.route('/searchbygenre/fantasy', methods=['post'])
def fantasy():
    ideal_book = "Harry Potter and the Sorcerer's Stone (Book 1)"
    return get_genre_books(ideal_book, 100)


@app.route('/searchbygenre/comedy', methods=['post'])
def comedy():
    ideal_book = "The Nanny Diaries: A Novel"
    return get_genre_books(ideal_book, 100)


@app.route('/searchbygenre/horror', methods=['post'])
def horror():
    ideal_book = "Midnight"
    return get_genre_books(ideal_book, 100)

@app.route('/searchbygenre/thriller', methods=['post'])
def thriller():
    ideal_book = "The Da Vinci Code"
    return get_genre_books(ideal_book, 100)


@app.route('/searchbygenre/romance', methods=['post'])
def romance():
    ideal_book = "The Notebook"
    return get_genre_books(ideal_book, 100)


@app.route('/searchbygenre/scifi', methods=['post'])
def scifi():
    ideal_book = "The Hitchhiker's Guide to the Galaxy"
    return get_genre_books(ideal_book, 100)


@app.route('/searchbygenre/dystopian', methods=['post'])
def dystopian():
    ideal_book = "The Handmaid's Tale"
    return get_genre_books(ideal_book, 100)













# @app.route('/searchbygenre/thriller', methods=['post'])
# def thriller():
#     ideal_book = "The Da Vinci Code"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)

# @app.route('/searchbygenre/romance', methods=['post'])
# def romance():
#     ideal_book = "The Notebook"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)

# @app.route('/searchbygenre/scifi', methods=['post'])
# def scifi():
#     ideal_book = "The Hitchhiker's Guide to the Galaxy"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)

# @app.route('/searchbygenre/dystopian', methods=['post'])
# def dystopian():
#     ideal_book = "The Handmaid's Tale"
#     matching_indices = np.where(pt.index == ideal_book)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)
#     print(data)
#     return render_template('searchbygenre.html',data=data)



@app.route('/surprise')
def surprise():
    return render_template('surprise.html')

# @app.route('/surprise', methods=['post'])
# def surprise_fn():
#     random_num = random.randint(0, 2 ** 9)
#     a = pt.index[random_num]
#     matching_indices = np.where(pt.index == a)[0]
#     index = matching_indices[0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:1]
#     data =[]
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#         data.append(item)
#     print(data)

#     return render_template('surprise.html',data=data)

@app.route('/surprise', methods=['post'])
def surprise_fn():
    random_num = random.randint(0, 2 ** 9)
    a = pt.index[random_num]
    matching_indices = np.where(pt.index == a)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=False)[0:1]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['ISBN'].values)) 
        data.append(item)
    print(data)

    return render_template('surprise.html', data=data)

@app.route('/urbooks')
def urbooks_ui():
    random_num = random.randint(500, 2 ** 9)
    print(random_num)
    a = pt.index[random_num]
    matching_indices = np.where(pt.index == a)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=False)[0:15]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['ISBN'].values)) 
        data.append(item)
    print(data)

    return render_template('urbooks.html', data=data)






#WIKIPEDIA PART STARTS YAHA

# Initialize Wikipedia API

wiki = wikipediaapi.Wikipedia(language='en',user_agent="MyBookApp/1.0 (your.email@example.com)")

@app.route('/book',methods=['post'])
# def wiki_work():
    # print("works")

def get_wikipedia_summary(book_title):
    page = wiki.page(book_title)
    if page.exists():
        return page.summary[:3000] + '...' if len(page.summary) > 300 else page.summary
    return "No description found."

def get_author_info(author_name):
    author_page = wiki.page(author_name)
    if author_page.exists():
        return author_page.summary[:3000] + '...' if len(author_page.summary) > 300 else author_page.summary
    return "No information found."

def get_other_books_by_author(author_name):
    other_books = [b for b in books if b['Book-Author'] == author_name]
    return other_books[:5]



@app.route("/book/<isbn>")
def book_detail(isbn):
    # Ensure 'books' is a valid DataFrame or list of dictionaries
    book = None

    # Case 1: If 'books' is a DataFrame
    if isinstance(books, pd.DataFrame):
        # Find the book by ISBN in books DataFrame
        matching_books = books[books['ISBN'] == isbn]
        if not matching_books.empty:
            # Get the first matching book (removes duplicates)
            book = matching_books.iloc[0].to_dict()

    # Case 2: If 'books' is a list of dictionaries
    elif isinstance(books, list):
        # Find the first book matching the ISBN from the list
        book = next((b for b in books if b['ISBN'] == isbn), None)

    # Check if the book exists
    if book:
        # Check if the following functions exist, and provide fallback values if not
        book_description = None
        author_info = None
        try:
            book_description = get_wikipedia_summary(book['Book-Title']) or "No description available"
        except NameError:
            book_description = "No description available"

        try:
            author_info = get_author_info(book['Book-Author']) or "No author info available"
        except NameError:
            author_info = "No author info available"

        # Get other books by the same author (removing duplicates by title)
        if isinstance(books, pd.DataFrame):
            # Use Pandas to get unique books by the same author
            other_books_by_author = books[books['Book-Author'] == book['Book-Author']]
            unique_books = other_books_by_author.drop_duplicates(subset=['Book-Title']).to_dict(orient='records')
        else:
            # If it's a list of dictionaries
            other_books_by_author = [b for b in books if b['Book-Author'] == book['Book-Author']]
            unique_books = {b['Book-Title']: b for b in other_books_by_author}.values()

        print(f"Requested ISBN: {isbn}")
        print(f"Book found: {book}")
        print(f"Book description: {book_description}")
        print(f"Author info: {author_info}")

        # Render the book detail page
        return render_template(
            'book_detail.html', 
            book=book, 
            book_description=book_description, 
            author_info=author_info, 
            other_books=list(unique_books)
        )
    
    # If the book wasn't found, return a 404 error
    else:
        return "Book not found", 404





    


# @app.route("/book/book[ISBN]")
# def book_detail(isbn):
#     book = next((b for b in books if b['ISBN'] == isbn), None)

#     if book:
#         book_description = get_wikipedia_summary(book['Book-Title'])  # Get description from Wikipedia
#         author_info = get_author_info(book['Book-Author'])
#         other_books = get_other_books_by_author(book['Book-Author'])

#         return render_template('book_detail.html', book=book, book_description=book_description,
#                                author_info=author_info, other_books=other_books)
#     else:
#         return "Book not found", 404



@app.route('/book/title/<book_title>')
def book_detail_by_title(book_title):
    # Search books_df by title to find the ISBN
    book = books_df[books_df['Book-Title'] == book_title]

    if not book.empty:
        # Get the first matching book
        isbn = book.iloc[0]['ISBN']
        return redirect(url_for('book_detail', isbn=isbn))
    else:
        return "Book not found", 404









@app.errorhandler(Exception)
def handle_exception(e):
    # Output all errors in the console
    print(f"Error: {e}")
    return e




if __name__ == '__main__':
    app.run(debug=True)
