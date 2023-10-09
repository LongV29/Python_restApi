from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
 
@app.route('/employee/create', methods=['POST'])
def create_employee():
    try:        
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']	
        _salary = _json['salary']	
 
        if _name and _email and _phone and _address and _salary and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO employee(name, email, phone, address, salary) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _address, _salary)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.close() 
            respone = jsonify('Employee created successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as err:
        print(err)
    finally:
        
        conn.close()          
    
@app.route('/employee')
def employee():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address, salary FROM employee")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()  
 
@app.route('/employee/<int:employee_id>')
def employee_details(employee_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address, salary FROM employee WHERE id =%s", employee_id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close() 
 
@app.route('/employee/update', methods=['PUT'])
def update_employee():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        _salary = _json['salary']
        if _name and _email and _phone and _address and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE employee SET name=%s, email=%s, phone=%s, address=%s, salary=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _salary, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close() 
 
@app.route('/employee/delete/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE id =%s", (employee_id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as err:
        print(err)
    finally:
        cursor.close() 
        conn.close()
        
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()