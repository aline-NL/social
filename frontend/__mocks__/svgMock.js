import React from 'react';

const SvgMock = React.forwardRef((props, ref) => (
  <svg ref={ref} {...props} />
));

export const ReactComponent = SvgMock;
export default 'SvgrURL';

// This mock allows you to test components that import SVG files
// by returning a simple React component instead of the actual SVG file.
