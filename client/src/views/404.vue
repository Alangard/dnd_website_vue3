<template>
    <div class="main-container">
        <div>
            <img src="../assets/404mimic.svg" alt="">
            <span>
                It's not a page, it's a mimic.<br>
                <span>Error 404.</span>
                <span> It's your fault.</span>
            </span>

        </div>
    </div>
    
</template>

<style lang="scss" scoped>
    .main-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #3a3a3c;
        height: 100vh;

        div{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #ffff;
            font-weight: 700;
            font-size: 24px;
            padding: 0 10%;

            img{
                height: 300px;
                width: 300px;
            }

            span{text-align: center;}
        }
    }
</style>