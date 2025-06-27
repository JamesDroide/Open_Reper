#backend/model_loader.py
from models.style_detector.chess_model import ChessStyleAnalyzer
from models.opening_recommender.opening_recommender_model import OpeningRecommender

analyzer = ChessStyleAnalyzer.load_model("models/style_detector/chess_model")
recommender = OpeningRecommender().load_model("models/opening_recommender/opening_recommender_model")