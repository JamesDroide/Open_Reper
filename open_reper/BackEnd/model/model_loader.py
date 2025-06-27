from models.style_detector.chess_model import ChessStyleAnalyzer
from models.opening_recommender.opening_recommender_model import OpeningRecommender
from models.defense_recommender.defense_recommender_model import DefenseRecommender

analyzer = ChessStyleAnalyzer.load_model("models/style_detector/chess_model")
recommender = OpeningRecommender().load_model("models/opening_recommender/opening_recommender_model")
defense_recommender = DefenseRecommender().load_model("models/defense_recommender/defense_recommender_model")