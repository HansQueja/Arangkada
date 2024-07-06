-- SIMPLE
SELECT *
FROM routes
ORDER BY route_length;

SELECT *
FROM routes
ORDER BY start_route, end_route;

SELECT *
FROM operators
ORDER BY name_of_operator;

-- MODERATE
-- Group routes by their starting point, then order by most number of same starting point
SELECT start_route, COUNT(*) count
FROM routes
GROUP BY start_route
HAVING count > 1
ORDER BY count DESC;

-- Vehicle count by manufacturer
SELECT manufacturer, COUNT(*) count
FROM vehicles
GROUP BY manufacturer
ORDER BY count DESC;

-- Vehicle count by Vehicle type
SELECT vehicle_type, COUNT(*) count
FROM vehicles
GROUP BY vehicle_type
ORDER BY count DESC;

-- Vehicles average revenue by manufacturer 
SELECT manufacturer, ROUND(AVG(revenue), 2) average_revenue
FROM vehicles
GROUP BY manufacturer
ORDER BY average_revenue DESC;

-- Vehicles average revenue of by vehicle_type 
SELECT vehicle_type, ROUND(AVG(revenue), 2) average_revenue
FROM vehicles
GROUP BY vehicle_type
ORDER BY average_revenue DESC;

-- Vehicles average revenue of by model 
SELECT model, ROUND(AVG(revenue), 2) average_revenue
FROM vehicles
GROUP BY model
ORDER BY average_revenue DESC;

-- Vehicles average revenue, by vehicle_type and manufacturer and model
SELECT vehicle_type, manufacturer, model, ROUND(AVG(revenue), 2) average_revenue
FROM vehicles
GROUP BY vehicle_type, manufacturer, model
ORDER BY vehicle_type, manufacturer, model;

-- Operators count grouped by occupation
SELECT occupation, COUNT(*) count
FROM operators
GROUP BY occupation;

-- DIFFICULT
-- Routes of a given operator name (input for name_of_operator)
SELECT o.operator_number, r.route_id, r.start_route, r.end_route
FROM operators o
JOIN vehicles v ON v.operator_number = o.operator_number
JOIN routes r ON r.route_id = v.route_id
WHERE o.name_of_operator = "Haruki Murakami";

-- Operators' number of operational units and total revenue

SELECT o.operator_number, o.name_of_operator, o.no_of_operational_units, SUM(v.revenue) "Total revenue"
FROM operators o
JOIN vehicles v ON o.operator_number = v.operator_number
GROUP BY o.operator_number
ORDER BY "Total revenue" DESC;

-- Total maintenance cost of vehicle compared to their revenue
SELECT v.plate_number, v.revenue,  (c.brake_system + c.clutch + c.tires + c.battery + c.bearings + 
     c.belt + c.fuel_filter + c.piston_ring + c.lights + c.body + c.electrical_system) "Total maintenance cost"
FROM vehicles v
JOIN components c ON c.model = v.model
ORDER BY revenue DESC;     

