//Quiry all the buttons by the class of update-cart
var updateBtns = document.getElementsByClassName('update-cart')

//Add event handler for each button within a loop
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){

        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }


        function addCookieItem(productId, action){
            console.log('Not logged in...')

            if (action == 'add'){
                if(cart[productId] == undefined){
                    cart[productId] = {'quantity':1}
                }
                else{
                    cart[productId]['quantity'] += 1
                }
            }

            if (action == 'remove'){
                cart[productId]['quantity'] -= 1

                if (cart[productId]['quantity'] <= 0){
                    console.log('Item Should be deleted')
                    delete cart[productId]
                }
            }
            console.log('Cart:', cart)
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
            location.reload()
        }
        // function that will update the order for the user
        function updateUserOrder(productId, action){
            console.log('User is authenticated, sending data....')

            var url = '/update_item/'

            //send the POST data to the update item url
            fetch(url, {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                //The data will be sending to the backend
                body:JSON.stringify({'productId': productId, 'action': action})
            })
            //return the response that we get after sending the data to the view 
            .then((response) =>{
                return response.json()
            })
            //console the data out
            .then((data) =>{
                console.log('data:', data)
                location.reload()
            })
        }



    })

}