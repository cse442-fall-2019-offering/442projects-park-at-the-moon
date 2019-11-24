import json


class TestServer:

    def test_main(self, client):

        """
        DISCLAIMER: I HAVEN'T YET BEEN ABLE TO FIGURE OUT HOW TO RESET
        THE APP CONTEXT, THESE WILL BE DESIGNED BETTER IN THE FUTURE
        :param client:
        :return:
        """
        lot = "Alumni A"
        spots = 0

        for i in range(spots, -1, -1):
            self.verify_spots(client, lot, i)
            response = client.get('/car-entered/' + lot)
            assert response.status_code == 200

        self.verify_spots(client, lot, 0)
        response = client.get('/car-entered/' + lot)
        assert response.status_code == 200
        self.verify_spots(client, lot, 0)

        for i in range(0, spots):
            self.verify_spots(client, lot, i)
            response = client.get('/car-exited/' + lot)
            assert response.status_code == 200

        self.verify_spots(client, lot, spots)
        response = client.get('/car-exited/' + lot)
        assert response.status_code == 200
        self.verify_spots(client, lot, spots)

        response = client.get('/car-exited/' + "asjhcbanjns")
        assert not json.loads(response.data)

    def verify_spots(self, client, lot, num_spots):

        response = client.get('/update_spots/1')
        store = json.loads(response.data)

        #TODO: NEEDS UPDATION DUE TO THE CHANGE IN ENDPOINTS
        assert response.status_code == 200