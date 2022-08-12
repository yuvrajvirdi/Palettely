from crypt import methods
from point import Point
from cluster import Cluster
from kmeans import KMeans
from PIL import Image
from flask import Flask, render_template, render_template_string, request

def get_points(file):
    img = Image.open(file)
    img.thumbnail((200, 400))
    img = img.convert("RGB")

    w, h = img.size

    points = []
    for count, colour in img.getcolors(w * h):
        for _ in range(count):
            points.append(Point(colour))
    
    return points

def rgb_to_hex(rgb):
    return '#%s' % ''.join(('%02x' % p for p in rgb))

def get_colours(filename, n_colours=3):
    points = get_points(filename)
    clusters = KMeans(n_clusters=n_colours).fit(points)
    clusters.sort(key=lambda c: len(c.points), reverse=True)
    rgbs = [map(int, c.center.coordinates) for c in clusters]
    return list(map(rgb_to_hex, rgbs))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcjkefb'

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.files)
    colours = []
    if request.files:
        image = request.files['image']
        n_colours = request.form.get('amount')
        '''img = Image.open(image)
        print(img.size)'''
        colours = get_colours(image, n_colours=int(n_colours))
        print(colours)

    return render_template("index.html", colours=colours)

@app.errorhandler(500)
def handle_500(e):
    error = 'Please enter valid inputs'
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
