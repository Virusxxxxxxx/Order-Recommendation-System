import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//为了方便测试，此处用vuex做全局数据
const store = new Vuex.Store({
	state: {
		userInfo: {},
		isLogin: false,
		orderType: 'takein',
		addresses: [{
			"id": 1,
			"user_id": 1,
			"name": "测试先生",
			"phone": "16666666666",
			"gender": 0,
			"address": "测试大厦",
			"complete_address": "上海市浦东新区",
			"description": "ABC1234",
			"latitude": "",
			"longitude": "",
			"is_default": 1
		}],
		address: {},
		remark: '不打包'
	},
	mutations: {
		SET_ORDER_TYPE(state, orderType) {
			state.orderType = orderType
		},
		SET_ADDRESS(state, address) {
			state.address = address
		},
		SET_REMARK(state, remark) {
			state.remark = remark
		},
		SET_USERINFO(state, userInfo) {
			state.userInfo = userInfo
		},
		SET_ISLOGIN(state, isLogin) {
			state.isLogin = isLogin
		}
	}
})

export default store
