import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>Используемые технологии</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="Технологии" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Backend</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                Python 3.12
              </li>
              <li className={styles.textItem}>
                Django 5.2
              </li>
              <li className={styles.textItem}>
                Django REST Framework
              </li>
              <li className={styles.textItem}>
                PostgreSQL
              </li>
            </ul>
          </div>
        </div>
        
        <div>
          <h2 className={styles.subtitle}>Frontend</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                JS
              </li>
              <li className={styles.textItem}>
                React
              </li>
            </ul>
          </div>
        </div>
        
        <div>
          <h2 className={styles.subtitle}>Другое</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                Docker / Podman
              </li>
              <li className={styles.textItem}>
                NGINX
              </li>
            </ul>
          </div>
        </div>
      </div>
      
    </Container>
  </Main>
}

export default Technologies

