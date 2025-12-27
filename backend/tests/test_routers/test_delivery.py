from src.schemas import deliveries
import pytest


def test_error_token(client):
    res = client.get("/deliveries/")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}

#for post delivery 
def test_post_delivery(authorized_client):

    res = authorized_client.post(
        "/deliveries/",
        json={
            "customer_phone": "+972541234567",
            "customer_id": "12345678",
            "customer_name": "John Doe",
            "customer_address": "tel aviv",
            "delivery_type": "string"
            
        }
    )
    assert res.status_code == 201
    new_delivery = deliveries.DeliveryPostOutput(**res.json())
    assert new_delivery.customer_id == "12345678"
    assert new_delivery.customer_phone == "+972541234567"
    assert new_delivery.customer_name == "John Doe"
    assert new_delivery.customer_address == "Tel Aviv-Yafo, Israel"
    assert new_delivery.delivery_type == "string"
    
#for incorrect address in post delivery
def test_incorrect_address_post(authorized_client):
    
    res = authorized_client.post(
        "/deliveries/",
        json={
            "customer_phone": "0541234567",  
            "customer_id": "12345678",
            "customer_name": "John Doe",
            "customer_address": "tee",
            "delivery_type": "string"
        }
    )
    data = res.json()
    error_detail = data["detail"][0]
    
    assert "Address not valid according to Google Maps" in error_detail["msg"]
    assert res.status_code == 422
   

def test_short_address_post(authorized_client):
          
    res = authorized_client.post(
        "/deliveries/",
        json={
            "customer_phone": "0541234567",  
            "customer_id": "12345678",
            "customer_name": "John Doe",
            "customer_address": "te",
            "delivery_type": "string",
        }
    )
    assert res.status_code == 422


    
#for normal user to get only their deliveries
def test_get_normal_deliveries(authorized_client,test_deliveries):
    res = authorized_client.get("/deliveries/")
    assert res.status_code == 200
    assert len(res.json()) == 2
   
    
#for admin user to get all deliveries from all users   
def test_get_admin_deliveries(authorized_admin_client,test_deliveries):
    res = authorized_admin_client.get("/deliveries/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_deliveries)
    

#for admin user to update a delivery status
def test_put_delivery(authorized_admin_client,test_deliveries):
    res = authorized_admin_client.put(f"/deliveries/{test_deliveries[1].id}",json={
        "status":"delivered"}
    )
    assert res.status_code == 200
    new_delivery = deliveries.DeliveryPutOutput(**res.json())
    assert new_delivery.status == "delivered"


#for incorrect status in put delivery for admin user
@pytest.mark.parametrize("status,id,status_code", [("new","2",422),
                                                           ("approve","1",400),
                                                           ("delivered","7",404)])
def test_incorrect_admin_put_delivery(authorized_admin_client,test_deliveries,status,status_code,id):
    res = authorized_admin_client.put(f"/deliveries/{id}",json={
        "status": status}
    )
    assert res.status_code == status_code
    
#for normal user to try to update a delivery
def test_incorrect_normal_put_delivery(authorized_client,test_deliveries):
    res = authorized_client.put("/deliveries/2",json={
        "status":"delivered"}
    )
    assert res.status_code == 403

#for normal user to delete only their delivery 
def test_delete_delivery(authorized_client,test_deliveries):
    res = authorized_client.delete(f"/deliveries/{test_deliveries[1].id}")
    assert res.status_code == 204

#trying to delete a delivery that does not exist and to delete a delivery that belongs to another user and not an admin
@pytest.mark.parametrize("id,status_code", [("30",404),("4",403)]) 

def test_incorrect_delete_delivery(authorized_client,test_deliveries,id,status_code):
    res = authorized_client.delete(f"/deliveries/{id}")
    assert res.status_code == status_code
    
#for admin user to delete any delivery from any user in the database
def test_delete_delivery_admin(authorized_admin_client,test_deliveries):
    res = authorized_admin_client.delete(f"/deliveries/{test_deliveries[3].id}")
    assert res.status_code == 204


