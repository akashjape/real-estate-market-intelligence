1. Removed duplicates based on 'listing_url', 'price_num', 'area_sqft'.
2. Handled 'Call for Price' of the price_raw column
3. Deleted those rows containing that word.
4. Validated 'price_num' column (Already in good condition)
5. Analyzed 'bhk_number' column -
	Found : na records (filled them - Studio Apartment with 1 BHK) & dropped 1 record
 