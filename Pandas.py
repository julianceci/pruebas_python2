import pandas as pd

avg_course_ratings = {
  "course_id": [24, 23, 46, 96, 56, 41],
  "rating": [4.65, 4.8, 4.8, 4.69, 4.66, 3.8]
}

courses_to_recommend = {
  "user_id": [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3],
  "course_id": [24, 23, 46, 46, 40, 41, 42, 43, 47, 46, 96, 56],
}

avg_course_ratings_df = pd.DataFrame(avg_course_ratings)
courses_to_recommend_df = pd.DataFrame(courses_to_recommend)

# Complete the transformation function
def transform_recommendations(avg_course_ratings, courses_to_recommend):
    # Merge both DataFrames
    merged = courses_to_recommend.merge(avg_course_ratings)
    # Sort values by rating and group by user_id
    grouped = merged.sort_values("rating", ascending=False).groupby("user_id")
    # Produce the top 3 values and sort by user_id
    recommendations = grouped.head(2).sort_values("user_id")
    final_recommendations = recommendations[["user_id", "course_id","rating"]]
    # Return final recommendations
    return final_recommendations

# Use the function with the predefined DataFrame objects
recommendations = transform_recommendations(avg_course_ratings_df, courses_to_recommend_df)
print(recommendations)
