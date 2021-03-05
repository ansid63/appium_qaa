class TestAndroidBasicInteractions():

    def test_should_send_keys_to_search_box_and_then_check_the_value(self, driver):
        search_box_element = driver.find_element_by_id('txt_query_prefill')
        search_box_element.send_keys('Hello world!')

        assert search_box_element.text == 'Hello w!'
