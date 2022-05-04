<template>
	<uni-popup ref="popup" type="bottom" @change="change">
		<view class="popup-content d-flex flex-column">
			<view class="d-flex justify-content-end">
				<image src="/static/images/common/clousex-big.png" class="close_btn" @tap="close"></image>
			</view>
			<view class="d-flex flex-fill flex-column justify-content-between">
				<view class="d-flex flex-column">
					<view class="font-size-extra-lg font-weight-bold text-color-base mb-30">欢迎登陆爱尚星球~</view>
					<view class="font-size-base text-color-assist">登录后享受更好的服务体验</view>
				</view>
				<view class="d-flex flex-column user-form">
					<list-cell line-right padding="30rpx">
						<view class="form-item">
							<view class="label">用户名</view>
							<input type="text" v-model="form.username" placeholder="请输入用户名"/>
						</view>
					</list-cell>
					<list-cell line-right padding="30rpx">
						<view class="form-item">
							<view class="label">密码</view>
							<input type="password" v-model="form.password" placeholder="请输入密码"/>
						</view>
					</list-cell>
				</view>
				<view class="d-flex flex-column">
					<button type="primary" class="w-100 font-size-lg mb-30" @tap="login()">一键登陆</button>
					<view class="text-center mb-30 font-size-sm text-color-assist">
						点击一键登陆爱尚点餐，即表示已阅读并同意<font class="text-color-primary">《爱尚隐私政策》</font>
					</view>
					<view class="text-center font-primary font-size-sm text-color-primary">《爱尚小程序服务指南》</view>
				</view>
			</view>
		</view>
	</uni-popup>
</template>

<script>
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import listCell from '@/components/list-cell/list-cell.vue'
	import { mapMutations } from 'vuex'
	
	export default {
		name: 'LoginPopup',
		components: {
			uniPopup,
			listCell
		},
		data(){
			return {
				form: {
					username: '',
					password: '',
				},
			}
		},
		props: {
			
		},
		methods: {
			...mapMutations(['SET_USERINFO', 'SET_ISLOGIN', 'SET_TOKEN']),
			open() {
				this.$refs['popup'].open()
			},
			close() {
				this.$refs['popup'].close()
			},
			change({show}) {
				this.$emit('change', show)
			},
			login() {
				if(this.form.username.length != 0 && this.form.password.length != 0){
					uni.request({
										url:"http://127.0.0.1:8000/User/login",
										data:{
										  "name": this.form.username,
										  "password": this.form.password
										},
										method:"POST",
										success: (res) => {
											//赋值
											if(res.data.code == 0){
												this.SET_USERINFO(this.form.username)
												this.SET_ISLOGIN(true)
												this.SET_TOKEN(res.data.token)
												this.close()
												uni.showToast({
													title: '登录成功',
												})
											}else if(res.data.code == -1){
												uni.showToast({
													title: '密码错误',
												})
											}else{
												uni.showToast({
													title: '注册失败',
												})
											}
										},
										fail: (err) => {
											uni.showToast({
												title: '网络错误',
											})
										}
									})
					return


				}

			}
		}
	}
</script>

<style lang="scss" scoped>
	.popup-content {
		background-color: #FFFFFF;
		border-radius: 24rpx 24rpx 0 0;
		height: 50vh;
		padding: 50rpx 40rpx;
	}
	
	.close_btn {
		width: 40rpx;
		height: 40rpx;
	}
	.user-form {
		.form-item {
			width: 100%;
			display: flex;
			align-items: center;
			
			.label {
				width: 160rpx;
			}
			
			input {
				flex: 1;
			}
			
			.radio {
				display: flex;
				margin-right: 50rpx;
				image {
					width: 40rpx;
					height: 40rpx;
					margin-right: 20rpx;
				}
			}
		}
	}
</style>
