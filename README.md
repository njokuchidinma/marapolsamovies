**Marapolsa Movies API**

Welcome to the Marapolsa Movies API! This API is designed for managing and interacting with a movies review website, allowing users to register, log in, view and interact with reviews, comment on content, and much more. The API also supports various administrative operations such as adding movies, reviews, and awards.

**Table of Contents**

    Overview
    Features
    Installation
    Usage
        Authentication
        Reviews
        Comments
        News & Awards
    API Documentation
    Error Handling
    Contributing
    License

**Overview**

    This API powers the backend of the Marapolsa Movies website. It enables users to create accounts, view and post reviews, comment on content, and interact with various sections of the website. The API also includes functionality for administrators to manage content like movies, awards, and news.
    Features

        User registration and authentication
        Password reset functionality
        Review creation, editing, and filtering (e.g., most popular, trending)
        Commenting on reviews, news, and awards
        Management of news articles, awards, and movie information
        Administrator and staff roles with varying permissions

**Installation**

    Clone the repository:
        git clone https://github.com/yourusername/marapolsa-movies-api.git

    Navigate to the project directory:
        cd marapolsa-movies-api

    Install the required dependencies:
        pip install -r requirements.txt

    Run migrations to set up the database:
        python manage.py migrate

    Create a superuser for the admin interface:
        python manage.py createsuperuser

    Start the development server:
        python manage.py runserver

**Usage**

    Authentication
    Users can register, log in, and manage their accounts. Administrators can create staff members and manage content through the admin interface.

    Reviews
    Users can view reviews, filter them by various criteria (e.g., most popular, trending), and post their own reviews if they are staff members.

    Comments
    Users can comment on reviews, news articles, and awards. Comments can be filtered and retrieved by content type.

    News & Awards
    News and awards can be managed by administrators and viewed by all users.

**API Documentation**

**Authentication Endpoints**
1. User Registration:
    POST /api/v1/register/
        Registers a new user.

    Request Body:
        {
          "username": "newuser",
          "email_address": "newuser@example.com",
          "password": "newuserpassword",
          "confirm_password": "newuserpassword"
        }

    Response:
        {
          "data": "User created successfully",
          "id": "user_id",
          "refresh": "refresh_token",
          "access": "access_token"
        }

2. Login
    POST /api/v1/login/
        Description: Authenticates the user and returns JWT tokens.
    
    Request Body:
        {
          "email_address": "user@example.com",
          "password": "userpassword"
        }

    Response:
        {
          "id": "user_id",
          "username": "user_name",
          "refresh": "refresh_token",
          "access": "access_token"
        }

3. Change Password
    POST /api/v1/change-password/
        Description: Allows an authenticated user to change their password.

    Request Body:
        {
          "old_password": "oldpassword",
          "new_password": "newpassword",
          "confirm_new_password": "newpassword"
        }

    Response:
        {
          "detail": "Password changed successfully."
        }

4. Forgot Password (Password Reset Request)
    POST /api/v1/forgot-password/
        Description: Initiates the password reset process by sending an email with a reset link.
    
    Request Body:
        {
          "email_address": "user@example.com"
        }

    Response:
        {
          "message":"New password sent to your email"
        }

5. Logout
    POST /api/v1/logout/
        Description: Logs out the user by invalidating the current refresh and access tokens.

    Request Body:
        {
          "refresh": "refresh_token"
        }

    Response:
        {
          "message": "Logged out successfully."
        }

**USER DETAILS**

1. User Profile Endpoints
    i. Get User Profile
        GET /api/v1/users/{id}/
            Retrieves a specific user's profile by their user ID (primary key).

        Request Parameters:
            id: The primary key (ID) of the user.

        Response:
            {
            "data": {
                "id": 1,
                "username": "exampleuser",
                "email_address": "exampleuser@example.com",
                "country": "USA",
                "date_joined": "2024-08-13T12:34:56Z"
                }
            }

    ii. Update User Profile
        PUT /api/v1/users/{id}/
            Updates a specific user's profile information.

        Request Parameters:
            id: The primary key (ID) of the user.

        Request Body:
            {
                "country": "UK"
            }

        Response:
            {
            "data": "User updated successfully"
            }

    iii. List All Users
        GET /api/v1/users/
            Lists all users or retrieves the current authenticated user's profile information.
        Response:
            {
                "data": [
                    {
                    "id": 1,
                    "username": "exampleuser1",
                    "email_address": "exampleuser1@example.com",
                    "country": "USA",
                    "date_joined": "2024-08-13T12:34:56Z"
                    },
                    {
                    "id": 2,
                    "username": "exampleuser2",
                    "email_address": "exampleuser2@example.com",
                    "country": "Canada",
                    "date_joined": "2024-08-14T09:45:23Z"
                    }
                ]
            }

2. User Dashboard

    GET /api/v1/user-dashboard/
        Description: Retrieves the current user's dashboard data, including liked and saved reviews, news, and awards, as well as the user's comments.

    Response:
        {
          "liked_reviews": [...],
          "saved_reviews": [...],
          "liked_news": [...],
          "saved_news": [...],
          "liked_awards": [...],
          "saved_awards": [...],
          "user_comments": [...]
        }

**LIKES, SAVES AND COMMENTS**
1. Toggle Like
    POST /api/v1/toggle-like/{model_name}/{object_id}/
        Description: Toggles like on a specific model object (e.g., Review, News, Award).

    Request Parameters:
        model_name: The name of the model (e.g., review, news, award).
        object_id: The ID of the object to like/unlike.

    Response:
        {
          "liked": true
        }

2. Toggle Save
    POST /api/v1/toggle-save/{model_name}/{object_id}/
        Description: Toggles save on a specific model object (e.g., Review, News, Award).

    Request Parameters:
        model_name: The name of the model (e.g., review, news, award).
        object_id: The ID of the object to save/unsave.

    Response:
        {
          "saved": true
        }

3. Add Comment
    POST /api/v1/add-comment/{model_name}/{object_id}/
        Description: Adds a comment to a specific model object (e.g., Review, News, Award).

    Request Parameters:
        model_name: The name of the model (e.g., review, news, award).
        object_id: The ID of the object to comment on.
        
    Request Body:
        {
        "content": "This is a comment."
        }

    Response:
        {
            "id": "comment_id",
            "content": "This is a comment.",
            "timestamp": "2024-08-13T12:34:56Z"
        }

4.  User Comments
    POST /api/v1/user-comments/{content_type}/{object_id}/
        Description: Allows the user to add a comment to a specific content type (e.g., review, news, award).
        
    Request Parameters:
        content_type: The type of content (e.g., review, news, award).
        object_id: The ID of the object the user is commenting on.

    Request Body:
        {
          "comment": "This is a user comment."
        }

    Response:
        {
          "id": "comment_id",
          "content": "This is a user comment.",
          "timestamp": "2024-08-13T12:34:56Z"
        }

**REVIEWS, AWARDS, NEWS, MOVIES**
1. Review Data Handler
    POST /api/v1/reviews/
        Description: Creates a new review.
    
    Request Body:
        {
            "title": "Review Title",
            "content": "Review content here...",
            "rating": 4.5
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Reviews
        GET /api/v1/reviews/
            Retrieves all reviews, ordered by the latest timestamp.

        Response:
        {
        "data": [
            {
            "id": 1,
            "title": "Great Movie",
            "content": "Movie",
            "review": "This movie was fantastic!",
            "publisher": "admin",
            "timestamp": "2024-08-14T09:45:23Z"
            },
            ...
        ]
        }
    
    iii. Update a Review
         PUT /api/v1/reviews/{id}/
            Updates an existing review by its ID.

        Request Parameters:
            id: The primary key (ID) of the review.

        Request Body:
            {
                "title": "Updated Review",
                "review": "Updated review text."
            }

        Response:
            {
              "data": "ok"
            }
    iv.  Delete a Review
        DELETE /api/v1/reviews/{id}/
            Deletes an existing review by its ID.
        Request Parameters:
            id: The primary key (ID) of the review.
        Response:
            Status 204 No Content.



2. Movie Data Handler
    POST /api/v1/movies/

        Description: Creates a new movie.
       
    Request Body:
        {
          "title": "Movie Title",
          "genre": "Drama",
          "industry": "Hollywood",
          "release_date": "2024-08-13",
          "streaming_platform": "Netflix"
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Movies
        GET /api/v1/movies/
            Retrieves all movies, ordered by the latest timestamp.
        
        Response:
            {
            "data": [
                {
                "id": 1,
                "title": "Inception",
                "description": "A mind-bending thriller.",
                "publisher": "admin",
                "timestamp": "2024-08-14T09:45:23Z"
                },
                ...
            ]
            }
    iii.  Update a Movie
          PUT /api/v1/movies/{id}/
            Updates an existing movie by its ID.
            
        Request Parameters:
            id: The primary key (ID) of the movie.
     
        Request Body:
            {
            "title": "Updated Movie Title"
            }

        Response:
            {
            "data": "ok"
            }

    iv. Delete a Movie
        DELETE /api/v1/movies/{id}/
            Deletes an existing movie by its ID.

        Request Parameters:
            id: The primary key (ID) of the movie.

        Response:
            Status 204 No Content.

3. News Data Handler
    POST /api/v1/news/
        Description: Creates a new news article.
        
    Request Body:
        {
          "title": "News Title",
          "content": "News content here...",
          "image": "https://example.com/image.jpg"
        }

    Response:
        {
          "data": "ok"
        }

    ii. Get All News
        GET /api/v1/news/
            Retrieves all news, ordered by the latest timestamp.
            
        Response
            {
            "data": [
                {
                "id": 1,
                "title": "New Movie Release",
                "content": "Exciting new movie released today!",
                "publisher": "admin",
                "timestamp": "2024-08-14T09:45:23Z"
                },
                ...
            ]
            }
    iii.  Update a News Article
            PUT /api/v1/news/{id}/
                Updates an existing news article by its ID.
                
            Request Parameters:
                id: The primary key (ID) of the news article.
            
            Request Body:
                {
                "title": "Updated News Title"
                }

            Response:
                {
                "data": "ok"
                }

    iv. Delete a News Article

            DELETE /api/v1/news/{id}/

                Deletes an existing news article by its ID.
                Request Parameters:
                    id: The primary key (ID) of the news article.
                Response:
                    Status 204 No Content.

4. Award Data Handler
    POST /api/v1/awards/
        Description: Creates a new award.
    
    Request Body:
        {
          "title": "Award Title",
          "description": "Award description here...",
          "date": "2024-08-13"
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Awards
        GET /api/v1/awards/
            Retrieves all awards, ordered by the latest timestamp.
            
        Response:
            {
            "data": [
                {
                "id": 1,
                "title": "Best Director",
                "description": "Awarded to the best director.",
                "publisher": "admin",
                "timestamp": "2024-08-14T09:45:23Z"
                },
                ...
            ]
            }
    
    iii. Update an Award
         PUT /api/v1/awards/{id}/
            Updates an existing award by its ID.
        
        Request Parameters:
            id: The primary key (ID) of the award.
        
        Request Body:
            {
            "title": "Best Actor Updated"
            }

        Response:
            {
            "data": "ok"
            }

    iv. Delete an Award
        DELETE /api/v1/awards/{id}/
            Deletes an existing award by its ID.
        Request Parameters:
            id: The primary key (ID) of the award.
        Response:
            Status 204 No Content.

5. Genre Data Handler
    POST /api/v1/genres/
        Description: Creates a new genre.
        
    Request Body:
        {
          "name": "Genre Name"
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Genres
        GET /api/v1/genres/
            Retrieves all genres.
            
        Response:
            {
                "data": [
                    {
                    "id": 1,
                    "name": "Action",
                    "description": "Action movies."
                    },
                    ...
            ]
            }
    
    iii. Update a Genre
         PUT /api/v1/genres/{id}/
            Updates an existing genre by its ID.
        
        Request Parameters:
            id: The primary key (ID) of the genre.
            
        Request Body:
            {
             "name": "Updated Genre Name"
            }

        Response:
            {
             "data": "ok"
            }

    iv. Delete a Genre
        DELETE /api/v1/genres/{id}/
            Deletes an existing genre by its ID.
        Request Parameters:
            id: The primary key (ID) of the genre.
        Response:
            Status 204 No Content.

6. Industry Data Handler
    POST /api/v1/industries/
        Description: Creates a new industry.
        
    Request Body:
        {
          "name": "Industry Name"
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Industries
        GET /api/v1/industries/
            Retrieves all industries.
            
        Response:
            {
                "data": [
                    {
                    "id": 1,
                    "name": "Hollywood",
                    },
                    ...
            ]
            }
    
    iii. Update an industry
         PUT /api/v1/industries/{id}/
            Updates an existing industry by its ID.
        
        Request Parameters:
            id: The primary key (ID) of the industry.
            
        Request Body:
            {
             "name": "Updated Industry Name"
            }

        Response:
            {
             "data": "ok"
            }

    iv. Delete a Industry
        DELETE /api/v1/industries/{id}/
            Deletes an existing industry by its ID.
        Request Parameters:
            id: The primary key (ID) of the industry.
        Response:
            Status 204 No Content.

7. Streaming Platform Data Handler
    POST /api/v1/streaming-platforms/
        Description: Creates a new streaming platform.
    
    Request Body:
        {
        "name": "Platform Name"
        }

    Response:
        {
          "data": "ok"
        }
    
    ii. Get All Streaming Platforms
        GET /api/v1/streaming-platforms/
            Retrieves all streaming platforms.
        
        Response:
            {
            "data": [
                {
                "id": 1,
                "name": "Netflix",
                },
                ...
            ]
            }
    iii. Update a Streaming Platform
         PUT /api/v1/streaming-platforms/{id}/
            Updates an existing streaming platform by its ID.

         Request Parameters:
            id: The primary key (ID) of the platform.
         Request Body:
            {
              "name": "Updated Platform Name"
            }
         Response:
            {
            "data": "ok"
            }

    iv. Delete a Streaming Platform
        DELETE /api/v1/streaming-platforms/{id}/
            Deletes an existing streaming platform by its ID.
        Request Parameters:
                id: The primary key (ID) of the platform.
        Response:
                Status 204 No Content.

8. Most Popular Reviews
    GET /api/v1/popular-reviews/
        Description: Retrieves a list of the most popular reviews based on likes, comments, and stars.
    
    Response:
        [
        {
            "id": "review_id",
            "title": "Popular Review Title",
            "content": "Review content here...",
            "likes": 120,
            "comments": 15,
            "stars": 4.8,
            "timestamp": "2024-08-13T12:34:56Z"
        },
        ...
        ]

9. Trending Reviews
    GET /api/v1/trending-reviews/
        Description: Retrieves a list of trending reviews based on recent activity.

    Response:
        [
        {
            "id": "review_id",
            "title": "Trending Review Title",
            "content": "Review content here...",
            "likes": 80,
            "comments": 10,
            "stars": 4.5,
            "timestamp": "2024-08-13T12:34:56Z"
        },
        ...
        ]

10. Suggested Reviews
    GET /api/v1/suggested-reviews/<uuid:review_id>/
        Description: Retrieves a list of suggested reviews for the current user based on their interests and previous interactions.

    Response:
        [
        {
            "id": "review_id",
            "title": "Suggested Review Title",
            "content": "Review content here...",
            "likes": 60,
            "comments": 8,
            "stars": 4.0,
            "timestamp": "2024-08-13T12:34:56Z"
        },
        ...
        ]

11. Newsletter Subscription
    POST /api/v1/newsletter-subscriptions/
        Subscribes a user to the newsletter.
    
    Request Body:
        {
          "email": "user@example.com"
        }

    Response:
        {
          "message": "Subscribed to newsletter"
        }

12. TV Show Reviews
    GET /api/v1/tvshow-reviews/
        Retrieves all reviews related to TV shows, paginated.
    Query Parameters:
        limit: Maximum number of reviews to return per page.
        offset: The starting position of the paginated query.
    Response:
        {
            "count": 100,
            "next": "http://api.example.com/tvshow-reviews/?limit=10&offset=10",
            "previous": null,
            "results": [
                {
                "id": 1,
                "title": "Amazing TV Show",
                "review": "This show was incredible!",
                "genre": "Drama",
                "publisher": "staff1",
                "timestamp": "2024-08-14T09:45:23Z"
                },
                ...
        ]
        }

13. Suggested Reviews
    GET /api/v1/suggested-reviews/{review_id}/
        Retrieves reviews that share the same genre as the specified review, excluding the original review and paginated.
    Request Parameters:
        review_id: The ID of the review for which suggestions are requested.
    Query Parameters:
        limit: Maximum number of reviews to return per page.
        offset: The starting position of the paginated query.
    Response:
        {
        "count": 50,
        "next": "http://api.example.com/suggested-reviews/{review_id}/?limit=10&offset=10",
        "previous": null,
        "results": [
            {
            "id": 2,
            "title": "Another Great Show",
            "review": "This show is just as great as the other one!",
            "genre": "Drama",
            "publisher": "admin",
            "timestamp": "2024-08-14T09:45:23Z"
            },
            ...
        ]
        }
