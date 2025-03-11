from flask import Flask, jsonify, request
import mysql.connector

app=Flask(__name__)



conn = mysql.connector.connect(
    host="localhost",        
    user="root",        
    password="Venu@2425",
    database="first_project" ,
)







@app.route('/users',methods=['GET'])
def get_users():
	cursor= conn.cursor()
	cursor.execute('SELECT * FROM users')
	data=cursor.fetchall()
	cursor.close()
	return jsonify(data)



@app.route('/adduser', methods=['POST'])
def add_user():
    print('Adding user...')

    try:
        
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"error": "Missing name or email"}), 400

        # Extract 'name' and 'email' from the JSON data
        name = data['name']
        email = data['email']

        # Insert the user into the database
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit() 
      
        cursor.close()

        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({"error": str(e)}), 400
 



@app.route('/updateuser/<int:id>', methods=['PUT', 'PATCH'])
def update_user(id):
    print(f"Updating user with ID {id}...")

    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if the required fields are present in the request data
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"error": "Missing name or email"}), 400
        
        name = data['name']
        email = data['email']

        # Create a cursor to execute the query
        cursor = conn.cursor()

        # Execute the UPDATE query
        cursor.execute('''
            UPDATE users
            SET name = %s, email = %s
            WHERE id = %s
        ''', (name, email, id))

        # Commit the changes to the database
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "User not found"}), 404
        
        # Close the cursor
        cursor.close()

        # Return a success message
        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as e:
        # Handle MySQL-specific errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        # Handle other types of errors (generic error handling)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400
    




if __name__ == '__main__':
    app.run(debug=True)









