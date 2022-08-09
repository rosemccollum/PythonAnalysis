function x_pred = ar_predict(x, nsamp, ar_params)
% ar_predict: predict future signal using given AR model parameters.
% syntax: x_pred = ar_predict(x, nsamp, ar_params)
%
% In:
%   x: past values of signal. If x is a matrix, operates on each column.
%   nsamp: number of future values to predict (length of output)
%
%   ar_params: parameters of the autoregressive model (vector), represented
%   as in the output of 'arburg' (for instance). If x is a matrix with
%   n columns, ar_params may be a vector or a matrix with n rows.
%
% Out:
%   x_pred: column vector of the predicted values, or matrix whose columns
%   correspond to the columns of the input matrix.
% 
% When applying the AR model, pads the beginning of x with zeros if
% necessary (i.e. if length(ar_params) > length(x)).

if isvector(x)
    x = x(:);
end

[lenx, nx] = size(x);
assert(isscalar(nsamp) && isreal(nsamp) && nsamp >= 0 && mod(nsamp, 1) == 0, ...
    'nsamp must be a positive integer');

if isvector(ar_params)
    ar_params = ar_params(:).';
else
    assert(size(ar_params, 1) == nx, 'Number of models does not match size of input');
end

ar_params_mod = -ar_params(:, 2:end).';
order = size(ar_params_mod, 1);

npad = max(0, order - lenx);
offset = npad + lenx;

x_ext = [zeros(npad, nx); x; zeros(nsamp, nx)];
for ksamp = 1:nsamp
    x_ext(offset + ksamp, :) = sum(ar_params_mod .* x_ext(offset + ksamp + (-1:-1:-order), :));
end

x_pred = x_ext(offset + (1:nsamp), :);

end