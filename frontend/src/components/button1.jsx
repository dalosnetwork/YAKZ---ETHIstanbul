import PropTypes from 'prop-types';
import Icon from './iconManager';
import click1 from '../design/sounds/Click 01.mp3';
import click2 from '../design/sounds/Click 02.mp3';
import click3 from '../design/sounds/Click 03.mp3';
import click4 from '../design/sounds/Click 04.mp3';

const soundFiles = [click1, click2, click3, click4];

const Button1 = ({
  onClick,
  label,
  className,
  iconName,
  img,
  imgClass,
  style,
  id
}) => {
  
  const handleMouseDown = () => {
    const src = soundFiles[Math.floor(Math.random() * soundFiles.length)];
    const audio = new Audio(src);
    audio.preload = 'auto';
    audio.play().catch(err => console.warn('play failed', err));
  };

  const handleClick = e => {
    onClick?.(e);
  };

  return (
    <button
      type="button" 
      id={id}
      className={`button1 ${className}`}
      style={{ position: 'relative' }}
      onMouseDown={handleMouseDown}
      onClick={handleClick}
    >
      <div className="outer" style={style}>
        {iconName ? (
          <Icon name={iconName} className={`placeholder my-auto ${imgClass}`} />
        ) : img ? (
          <img
            src={img}
            className={`placeholder my-auto me-2 ${imgClass}`}
            style={{ height: '24px' }}
            alt=""
          />
        ) : null}
        {label}
      </div>
      <div className="inner"></div>
    </button>
  );
};

Button1.propTypes = {
  onClick: PropTypes.func,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  className: PropTypes.string,
  img: PropTypes.string,
  imgClass: PropTypes.string,
  id: PropTypes.string
};

export default Button1;
