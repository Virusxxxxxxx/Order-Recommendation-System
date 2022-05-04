<template>
	<view class="container">
		<view class="bg"></view>
		<view class="main">
			<view class="info">
				<image class="avatar" src="https://bpic.51yuansu.com/pic3/cover/00/87/19/58dafa13037b8_610.jpg?x-oss-process=image/sharpen,100"></image>
				<view class="name">支付成功</view>
			</view>
			<view class="code-section">
				<view class="mb-20">订单号：{{this.$route.query.id}}</view>
				<view class="tips">若有订单异常，请凭订单号询问前台</view>
			</view>
		</view>
	</view>
</template>

<script>
</script>

<style lang="scss" scoped>
.container {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	background-color: #FFFFFF;
}

.bg {
	background-color: #424141;
	height: 25vh;
	/* #ifdef H5 */
	height: calc(25vh - 44px);
	/* #endif */
}

.main {
	flex: 1;
	display: flex;
	flex-direction: column;
}

.info {
	display: flex;
	flex-direction: column;
	align-items: center;
	border-bottom: 1rpx solid rgba($color: $border-color, $alpha: 0.6);
	
	.avatar {
		position: relative;
		width: 140rpx;
		height: 140rpx;
		border-radius: 100%;
		margin-top: -70rpx;
		margin-bottom: 20rpx;
	}
	
	.name {
		font-size: $font-size-extra-lg;
		font-weight: bold;
		margin-bottom: 50rpx;
	}
	
	.desc {
		font-size: $font-size-sm;
		color: $text-color-assist;
		margin-bottom: 20rpx;
	}
}

.code-section {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	font-size: $font-size-base;
	color: $font-size-base;
	
	.tips {
		font-size: $font-size-sm;
		color: $text-color-assist;
	}
}
</style>

