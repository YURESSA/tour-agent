from app.controllers.constructor.crud import CRUD
from app.models.booking import Booking

bookings_crud = CRUD(Booking)
