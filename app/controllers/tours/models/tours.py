from app.controllers.constructor.crud import CRUD
from app.models.tour import Tour


class TourCRUD(CRUD):
    def __init__(self, model=Tour):
        super().__init__(model)

    def filter_tours(self, filters):
        query = self.model.query

        if 'country' in filters:
            query = query.filter(self.model.country.ilike(f"%{filters['country']}%"))
        if 'city' in filters:
            query = query.filter(self.model.city.ilike(f"%{filters['city']}%"))
        if 'hotel' in filters:
            query = query.filter(self.model.hotel.ilike(f"%{filters['hotel']}%"))
        if 'date' in filters:
            query = query.filter(self.model.date == filters['date'])
        if 'min_cost' in filters:
            query = query.filter(self.model.cost >= float(filters['min_cost']))
        if 'max_cost' in filters:
            query = query.filter(self.model.cost <= float(filters['max_cost']))

        return query.all()


tour_crud = TourCRUD()
