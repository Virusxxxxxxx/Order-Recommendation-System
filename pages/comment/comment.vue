<template>
	<view class="container">
		<view class="section">
			<view class="d-flex justify-content-between align-items-center pt-40 pb-40">
				<view class="font-size-lg font-weight-bold">菜品：{{ this.$route.query.cname }}</view>
			</view>
			<view class="experience-card">
				<view>
					<text class="text-color-assist font-size-lg font-weight-bold">请评分：</text>
					<view class="pt-40">
						<uni-rate v-model="rateValue" @change="onChangeRate" :max="5" :value="5" :margin="18" />
					</view>
				</view>
			</view>
			<view style="height: 1px;"></view>
		</view>
		<view class="section">
			<view style="height: 10px;"></view>
			<button type="primary" @tap="submit()">
				提交
			</button>
			<view style="height: 10px;"></view>
		</view>
		<!-- <image src="https://static.heytea.com/taro_trial/v1/img/my/member_benefits/level_1-6_bg.png"></image> -->
	</view>
</template>

<script>
	import listCell from '@/components/list-cell/list-cell.vue'
	import { mapState } from 'vuex'
	export default {
		components: {
			listCell
		},
		computed: {
			...mapState(['userInfo'])
		},
		data() {
			return {
				rateValue: 5,
			}
		},
		methods: {
			submit() {
				uni.request({
					url: "http://127.0.0.1:8000/Comment/commentMeal/"+this.$store.state.token,
					method: 'POST',
					data: {
						score: this.rateValue,
						meal_id: this.$route.query.cid,
						content: "default"
					},
					success: (res) => {
							// console.log(res.data)
							if(res.data.code == 0){
								uni.showToast({
									title: "评论成功"
								})
							}else{
								uni.showToast({
									title: "内部错误"
								})
							}
						}
				});
			},
			onChangeRate(e) {
				this.rateValue=JSON.stringify(e.value)
			}
		}
	}
</script>

<style lang="scss" scoped>
.section {
	background-color: #ffffff;
	padding: 0 40rpx;
	margin-bottom: 20rpx;
}

.member-btn {
	font-size: $font-size-sm;
	line-height: 1.8888;
}

.about-icon {
	width: 50rpx;
	height: 50rpx;
}

.experience-card {
	width: 100%;
	height: 270rpx;
	background-color: #ffffff;
	background-image: url('https://static.heytea.com/taro_trial/v1/img/my/member_benefits/me_rights_img_go.png');
	background-repeat:no-repeat;
	background-size: 100% 100%;
	border-radius: $border-radius-lg;
	box-shadow: 0 0 20rpx 0 rgba($color: $border-color, $alpha: 0.4);
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	padding: 40rpx;
	margin-bottom: 40rpx;
	
	.level {
		font-size: 40rpx;
		font-family: 'neutra';
		margin-right: 10rpx;
	}
	
	.process-box {
		margin-top: 10rpx;
		width: 50%;
	}
}

.benefit-card {
	padding-bottom: 30rpx;
	.header {
		padding: 20rpx 0;
		display: flex;
		align-items: center;
		
		.title {
			font-size: $font-size-lg;
			font-family: 'wenyue';
		}
	}
	
	.grid {
		display: flex;
		flex-wrap: wrap;
		
		.item {
			width: 33.3333%;
			display: flex;
			flex-direction: column;
			align-items: center;
			font-size: $font-size-sm;
			margin: 34rpx 0;
			
			.image {
				width: 64rpx;
				height: 64rpx;
				margin-bottom: 14rpx;
			}
		}
	}
}
</style>

