## Example

### fastapi_cls demo
- Create a file `view.py` with: 

    ```python
    from pydantic import BaseModel

    from fastapi import Depends

    class User(BaseModel):
        username: str
        email: Optional[str] = None
        full_name: Optional[str] = None
        disabled: Optional[bool] = None

    async def get_user():
        return User(username="john")

    class ItemView:
        user: User = Depends(get_user)

        def get(self) -> User:
            return self.user

        def post(self) -> str:
            self.user.username = 'change name'
            return "ok"
    
    ``` 
- Create a file `route.py` with: 
    ```python
    from fastapi_cls import ClassRouter 
    router = ClassRouter()
    router.add_resource("/item",ItemView,methods=["GET","POST"])    
    ``` 
    Or, if you want to define your owner method reflect to http method. you can do like this. 

    ```python
    from fastapi_cls import ClassRouter 
    router = ClassRouter()
    router.add_method_route("/item",ItemView,ItemView.get, methods=["GET"])    
    router.add_method_route("/item",ItemView,ItemView.post, methods=["POST"])    
    ```

###  Its equivalent to 
- fastapi
    ```python
    from fastapi import ApiRouter, Depends


    class User(BaseModel):
        username: str
        email: Optional[str] = None
        full_name: Optional[str] = None
        disabled: Optional[bool] = None

    async def get_user():
        return User(username="john")

    router = ApiRouter()

    @router.get('/item')
    def get(user: User = Depends(get_user)) -> User:
        return user

    @router.post('/item')
    def post(user: User = Depends(get_user)) -> str:
        user.username = 'change name'
        return "ok"
    ```

    In this case. The `ItemView` methods `get` and `post` will bind on router as a function.