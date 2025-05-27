import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Коротко о проекте</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что это за сайт?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Foodgram - это веб-приложение и API, созданные в рамках курса "Бэкенд-разработка" в РТУ МИРЭА(В партнёрстве с Яндекс Практикумом).
            </p>
            <p className={styles.textItem}>
              Авторизованные пользователи могут публиковать рецепты, добавлять понравившиеся рецепты в избранное, подписываться на публикации других авторов и формировать список покупок для выбранных рецептов.
            </p>
            <p className={styles.textItem}>
              Любые посетители сайта могут изучить каталог рецептов.
            </p>
            <p className={styles.textItem}>
              Чтобы использовать все возможности сайта — нужна регистрация. Заходите и делитесь своими любимыми рецептами!
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Код проекта находится тут - <a href="https://github.com/MorganBlack777/foodgram-st" className={styles.textLink}>Github</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="https://github.com/MorganBlack777" className={styles.textLink}>Ежов Арсений</a>
            </p>
          </div>
        </aside>
      </div>
      
    </Container>
  </Main>
}

export default About

