# from crypt import methods
# from dbm import error

import logging
logging.basicConfig(level=logging.DEBUG)


from flask import Flask,render_template,request
import pickle
import numpy as np
import random
import wikipediaapi

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# with open('books.pkl', 'rb') as f:
#     books_df = pickle.load(f)
#     bookslist = books_df.to_dict(orient='records')

print(f"Type of books: {type(books)}")
print("First few entries in books:")
print(books[:5])

app = Flask(__name__)







@app.route('/')
def index():
    return render_template('index.html')



@app.route('/top50')
def top50():
    # bookslist = popular_df.to_dict(orient='records')
    return render_template('top50.html',
                           books = popular_df.to_dict(orient='records'),
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
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

    # similar books on the similarity scores for the matched book
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:4]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


@app.route('/searchbygenre')
def searchbygenre():
    return render_template('searchbygenre.html')

@app.route('/searchbygenre/fantasy', methods=['post'])
def fantasy():
    ideal_book = "Harry Potter and the Sorcerer's Stone (Book 1)"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)


@app.route('/searchbygenre/comedy', methods=['post'])
def comedy():
    ideal_book = "The Nanny Diaries: A Novel"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)

@app.route('/searchbygenre/horror', methods=['post'])
def horror():
    ideal_book = "Midnight"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)

@app.route('/searchbygenre/thriller', methods=['post'])
def thriller():
    ideal_book = "The Da Vinci Code"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)

@app.route('/searchbygenre/romance', methods=['post'])
def romance():
    ideal_book = "The Notebook"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)

@app.route('/searchbygenre/scifi', methods=['post'])
def scifi():
    ideal_book = "The Hitchhiker's Guide to the Galaxy"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)

@app.route('/searchbygenre/dystopian', methods=['post'])
def dystopian():
    ideal_book = "The Handmaid's Tale"
    matching_indices = np.where(pt.index == ideal_book)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:100]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('searchbygenre.html',data=data)



@app.route('/surprise')
def surprise():
    # random_num = random.randint(0, 2 ** 9)
    # print(pt.index[random_num])
    return render_template('surprise.html')

@app.route('/surprise', methods=['post'])
def surprise_fn():
    random_num = random.randint(0, 2 ** 9)
    a = pt.index[random_num]
    matching_indices = np.where(pt.index == a)[0]
    index = matching_indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:1]
    data =[]
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)

    return render_template('surprise.html',data=data)


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



@app.route('/book/<string:isbn>', methods=['GET'])
def book_detail(isbn):
    print(f"Requested ISBN: {isbn}")  # Debugging line
    book = next((b for b in books if b['ISBN'] == isbn), None)

    if book:
        print(f"Found Book: {book}")  # Debugging line
        book_description = get_wikipedia_summary(book['Book-Title'])
        author_info = get_author_info(book['Book-Author'])
        other_books = get_other_books_by_author(book['Book-Author'])

        popular_df = [b for b in books if b['Book-Author'] == book['Book-Author']]
        book_name = list(b['Book-Title'] for b in popular_df)
        author = list(b['Book-Author'] for b in popular_df)
        image = list(b['Image-URL-M'] for b in popular_df)
        votes = list(b.get('num-ratings', 0) for b in popular_df) 
        rating = list(b.get('avg_rating', 0) for b in popular_df)

        return render_template('book_detail.html', book=book, book_description=book_description,
                                author_info=author_info, other_books=other_books, book_name=book_name,
                                author_list=author, image=image, votes=votes, rating=rating)
    else:
        print(f"Book not found for ISBN: {isbn}")
        return "Book not found", 404









@app.errorhandler(Exception)
def handle_exception(e):
    # Output all errors in the console
    print(f"Error: {e}")
    return e




if __name__ == '__main__':
    app.run(debug=True)