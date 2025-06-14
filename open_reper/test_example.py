import pytest
from open_reper.model_loader import analyzer, recommender

pgn = """
[Event "Rated blitz game"]
[Site "https://lichess.org/p9pF1UIZ"]
[Date "2025.05.19"]
[White "Noc_sniper"]
[Black "bell505"]
[Result "1-0"]
[GameId "p9pF1UIZ"]
[UTCDate "2025.05.19"]
[UTCTime "03:47:42"]
[WhiteElo "2099"]
[BlackElo "2092"]
[WhiteRatingDiff "+6"]
[BlackRatingDiff "-6"]
[Variant "Standard"]
[TimeControl "180+0"]
[ECO "B13"]
[Opening "Caro-Kann Defense: Panov Attack"]
[Termination "Normal"]
[Annotator "lichess.org"]

1. c4 { [%eval 0.12] [%clk 0:03:00] } 1... c6 { [%eval 0.23] [%clk 0:03:00] } 2. e4 { [%eval 0.1] [%clk 0:02:58] } 2... d5 { [%eval 0.0] [%clk 0:02:59] } 3. exd5 { [%eval 0.04] [%clk 0:02:58] } 3... cxd5 { [%eval 0.14] [%clk 0:02:59] } 4. d4 { [%eval 0.12] [%clk 0:02:58] } { B13 Caro-Kann Defense: Panov Attack } 4... Nf6 { [%eval 0.07] [%clk 0:02:57] } 5. Nf3 { [%eval 0.0] [%clk 0:02:58] } 5... Bg4 { [%eval 0.14] [%clk 0:02:55] } 6. Nc3 { [%eval 0.17] [%clk 0:02:57] } 6... e6 { [%eval 0.22] [%clk 0:02:53] } 7. Be3 { [%eval 0.14] [%clk 0:02:55] } 7... Be7 { [%eval 0.18] [%clk 0:02:50] } 8. Be2 { [%eval -0.1] [%clk 0:02:54] } 8... O-O { [%eval 0.03] [%clk 0:02:47] } 9. O-O { [%eval -0.17] [%clk 0:02:51] } 9... a6 { [%eval 0.07] [%clk 0:02:43] } 10. h3 { [%eval 0.11] [%clk 0:02:51] } 10... Bh5 { [%eval 0.16] [%clk 0:02:42] } 11. Ne5 { [%eval 0.01] [%clk 0:02:48] } 11... Bxe2 { [%eval 0.11] [%clk 0:02:40] } 12. Qxe2 { [%eval -0.03] [%clk 0:02:48] } 12... Nc6 { [%eval 0.17] [%clk 0:02:39] } 13. Rac1 { [%eval 0.21] [%clk 0:02:46] } 13... dxc4 { [%eval 0.42] [%clk 0:02:33] } 14. Rfd1 { [%eval 0.0] [%clk 0:02:45] } 14... Nd5 { [%eval 0.14] [%clk 0:02:27] } 15. Qxc4? { (0.14 → -1.16) Mistake. Nxc6 was best. } { [%eval -1.16] [%clk 0:02:40] } (15. Nxc6 bxc6) 15... Nxe3 { [%eval -1.2] [%clk 0:02:23] } 16. fxe3 { [%eval -1.37] [%clk 0:02:40] } 16... Rc8? { (-1.37 → -0.23) Mistake. Nxe5 was best. } { [%eval -0.23] [%clk 0:02:20] } (16... Nxe5 17. dxe5 Qb6 18. Qf4 Qxb2 19. Ne4 Rad8 20. Rf1 Rd7 21. a4 h6 22. Kh2) 17. Nxc6 { [%eval -0.52] [%clk 0:02:38] } 17... Rxc6 { [%eval -0.55] [%clk 0:02:19] } 18. Qb3 { [%eval -0.4] [%clk 0:02:37] } 18... b5?! { (-0.40 → 0.15) Inaccuracy. Rb6 was best. } { [%eval 0.15] [%clk 0:02:17] } (18... Rb6) 19. Ne4 { [%eval -0.35] [%clk 0:02:32] } 19... Qb6 { [%eval -0.23] [%clk 0:02:11] } 20. Qd3 { [%eval -0.19] [%clk 0:02:29] } 20... Rfc8 { [%eval -0.3] [%clk 0:02:09] } 21. Rxc6 { [%eval -0.32] [%clk 0:02:27] } 21... Qxc6 { [%eval -0.2] [%clk 0:02:04] } 22. Rd2?! { (-0.20 → -0.82) Inaccuracy. Nc5 was best. } { [%eval -0.82] [%clk 0:02:22] } (22. Nc5) 22... f5?! { (-0.82 → -0.15) Inaccuracy. Qc1+ was best. } { [%eval -0.15] [%clk 0:01:49] } (22... Qc1+ 23. Kf2 Qh1 24. Kf3 Bh4 25. Rc2 Rd8 26. Qe2 Qh2 27. Kg4 Be7 28. Kf3) 23. Nc3 { [%eval -0.56] [%clk 0:02:11] } 23... Bd6?! { (-0.56 → -0.01) Inaccuracy. Qc7 was best. } { [%eval -0.01] [%clk 0:01:46] } (23... Qc7 24. Rd1) 24. e4?? { (-0.01 → -2.08) Blunder. d5 was best. } { [%eval -2.08] [%clk 0:02:05] } (24. d5 Qe8 25. dxe6 Bc5 26. Nd5 Qxe6 27. Rc2 Bd6 28. Rxc8+ Qxc8 29. Kf2 Kf7) 24... fxe4?? { (-2.08 → -0.06) Blunder. b4 was best. } { [%eval -0.06] [%clk 0:01:35] } (24... b4 25. Nd1 fxe4 26. Qe3 h6 27. Re2 e5 28. Qb3+ Kh8 29. d5 Qc1 30. g3) 25. Nxe4 { [%eval -0.23] [%clk 0:02:05] } 25... Bf4 { [%eval -0.06] [%clk 0:01:29] } 26. Rd1 { [%eval -0.14] [%clk 0:01:54] } 26... h6? { (-0.14 → 1.10) Mistake. Qd5 was best. } { [%eval 1.1] [%clk 0:01:24] } (26... Qd5 27. Nc3) 27. g3? { (1.10 → -0.30) Mistake. Nf6+ was best. } { [%eval -0.3] [%clk 0:01:51] } (27. Nf6+ Kf7) 27... Bb8 { [%eval -0.15] [%clk 0:01:22] } 28. Nc5?! { (-0.15 → -1.20) Inaccuracy. d5 was best. } { [%eval -1.2] [%clk 0:01:45] } (28. d5 exd5 29. Qxd5+ Qxd5 30. Rxd5 Kf7 31. Rd2 Ke6 32. Kg2 Ke5 33. Nc3 Rc6) 28... Qd6?! { (-1.20 → -0.26) Inaccuracy. e5 was best. } { [%eval -0.26] [%clk 0:01:16] } (28... e5) 29. Kg2 { [%eval -0.28] [%clk 0:01:37] } 29... Ba7 { [%eval 0.0] [%clk 0:01:09] } 30. b4 { [%eval -0.34] [%clk 0:01:35] } 30... Rd8 { [%eval 0.0] [%clk 0:00:53] } 31. Qe4 { [%eval 0.0] [%clk 0:01:30] } 31... Rc8?! { (0.00 → 0.96) Inaccuracy. e5 was best. } { [%eval 0.96] [%clk 0:00:47] } (31... e5 32. Qf3 Bxc5 33. bxc5 Qc7 34. dxe5 Rxd1 35. Qxd1 Qxc5 36. Qd8+ Kh7 37. Qd6) 32. Rd2?! { (0.96 → 0.07) Inaccuracy. Re1 was best. } { [%eval 0.07] [%clk 0:01:18] } (32. Re1 a5 33. a3 Re8 34. h4 Bb8 35. Re3 Ba7 36. Kh3 axb4 37. axb4 Qf8) 32... Re8?! { (0.07 → 0.74) Inaccuracy. e5 was best. } { [%eval 0.74] [%clk 0:00:44] } (32... e5 33. Qxe5 Bxc5 34. Rc2 Qc6+ 35. d5 Qg6 36. Qe6+ Qxe6 37. dxe6 Kf8 38. Rxc5) 33. Re2 { [%eval 0.79] [%clk 0:01:12] } 33... Kf7 { [%eval 1.27] [%clk 0:00:42] } 34. Qb7+ { [%eval 1.08] [%clk 0:01:07] } 34... Re7 { [%eval 1.02] [%clk 0:00:40] } 35. Qf3+ { [%eval 0.92] [%clk 0:00:59] } 35... Kg8 { [%eval 0.84] [%clk 0:00:39] } 36. Qg4?! { (0.84 → 0.26) Inaccuracy. Qe4 was best. } { [%eval 0.26] [%clk 0:00:45] } (36. Qe4 a5) 36... Bxc5?! { (0.26 → 0.89) Inaccuracy. Qd5+ was best. } { [%eval 0.89] [%clk 0:00:35] } (36... Qd5+) 37. bxc5?! { (0.89 → 0.10) Inaccuracy. dxc5 was best. } { [%eval 0.1] [%clk 0:00:44] } (37. dxc5 Qd1 38. h4 Re8 39. Qe4 e5 40. Rf2 Qd8 41. Rc2 Qd1 42. c6 Rd8) 37... Qd5+ { [%eval 0.02] [%clk 0:00:33] } 38. Qe4 { [%eval 0.07] [%clk 0:00:43] } 38... Qc4?? { (0.07 → 3.49) Blunder. Kf8 was best. } { [%eval 3.49] [%clk 0:00:28] } (38... Kf8) 39. Qa8+? { (3.49 → 1.61) Mistake. c6 was best. } { [%eval 1.61] [%clk 0:00:36] } (39. c6 Qb4 40. d5 Qc5 41. dxe6 Qd6 42. Qc2 Qc7 43. Qc5 b4 44. h4 a5) 39... Kh7 { [%eval 1.92] [%clk 0:00:27] } 40. Qe4+ { [%eval 1.69] [%clk 0:00:34] } 40... Kg8?? { (1.69 → 3.98) Blunder. g6 was best. } { [%eval 3.98] [%clk 0:00:25] } (40... g6 41. h4) 41. Rc2?? { (3.98 → 0.17) Blunder. c6 was best. } { [%eval 0.17] [%clk 0:00:29] } (41. c6 Rc7 42. Qxe6+ Qxe6 43. Rxe6 Kf7 44. d5 Re7 45. Rd6 b4 46. Kf3 a5) 41... Qb4?? { (0.17 → 2.43) Blunder. Qd5 was best. } { [%eval 2.43] [%clk 0:00:22] } (41... Qd5) 42. c6 { [%eval 2.12] [%clk 0:00:27] } 42... Rc7?? { (2.12 → 5.72) Blunder. Qd6 was best. } { [%eval 5.72] [%clk 0:00:18] } (42... Qd6 43. Qe5 Qxe5 44. dxe5 Re8 45. Kf3 Kf7 46. Ke4 Rd8 47. h4 g6 48. Rf2+) 43. Qxe6+ { [%eval 4.99] [%clk 0:00:26] } 43... Kh8 { [%eval 5.8] [%clk 0:00:18] } 44. Qe5 { [%eval 5.56] [%clk 0:00:24] } 44... Qa4 { [%eval 6.52] [%clk 0:00:11] } 45. Rf2 { [%eval 6.42] [%clk 0:00:21] } 45... Rc8 { [%eval 6.49] [%clk 0:00:06] } 46. Qe6 { [%eval 5.99] [%clk 0:00:16] } 46... Rg8 { [%eval 7.34] [%clk 0:00:06] } 47. c7 { [%eval 7.29] [%clk 0:00:15] } 47... Qxd4 { [%eval 8.35] [%clk 0:00:03] } 48. c8=Q { [%eval 7.99] [%clk 0:00:13] } 48... Qd3? { (7.99 → Mate in 1) Checkmate is now unavoidable. Qd5+ was best. } { [%eval #1] [%clk 0:00:01] } (48... Qd5+ 49. Qxd5 Rxc8 50. Qf7 Rd8 51. Re2 Kh7 52. Re8 Rxe8 53. Qxe8 b4 54. Qe4+) 49. Qcxg8# { [%clk 0:00:12] } { White wins by checkmate. } 1-0
"""

style_white = "Posicional"

def test_detect_style_white_player():
    assert analyzer.detect_style(pgn, "white") == {"status": "success", "style": "Posicional"}

def test_detect_style_black_player():
    assert analyzer.detect_style(pgn, "black") == {"status": "success", "style": "Posicional"}
    
def test_recommendation_white_player():
    assert recommender.recommend_for_pgn(pgn, "white", "posicional") == [{"apertura" : "Catalana", "probabilidad" : 0.78}, {"apertura" : "Italiana", "probabilidad" : 0.22}, {"apertura" : "Escocesa", "probabilidad" : 0.00}]
    
def test_recommendation_black_player():
    assert recommender.recommend_for_pgn(pgn, "black", "posicional") == [{"apertura" : "Londres", "probabilidad" : 0.98}, {"apertura" : "Escocesa", "probabilidad" : 0.02}, {"apertura" : "Catalana", "probabilidad" : 0.00}]